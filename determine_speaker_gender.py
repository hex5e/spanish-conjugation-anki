import argparse
import asyncio
import json
import re
import sqlite3

from openai import AsyncOpenAI, RateLimitError

MODEL = "gpt-4.1"
MAX_COMPLETION_TOKENS = 1024

parser = argparse.ArgumentParser(
    description="Determine speaker gender from example sentences"
)
parser.add_argument(
    "--start", type=int, default=1, help="1-indexed start row (inclusive)"
)
parser.add_argument(
    "--end", type=int, help="1-indexed end row (inclusive; defaults to all rows)"
)
parser.add_argument(
    "--workers", type=int, default=5, help="Number of concurrent OpenAI requests"
)
cli_args = parser.parse_args()

print_lock = asyncio.Lock()


async def log(card_id: int | str, text: str) -> None:
    async with print_lock:
        print(f"[{card_id}] {text}", flush=True)


def parse_retry_after(message: str) -> float | None:
    match = re.search(r"Please try again in (\d+)(ms|s)", message)
    if match:
        value = int(match.group(1))
        return value / 1000 if match.group(2) == "ms" else float(value)
    return None


async def openai_chat_with_retry(card_id: int | str, **kwargs):
    backoff = 1.0
    while True:
        try:
            async with sem:
                return await client.chat.completions.create(**kwargs)
        except RateLimitError as e:
            wait = parse_retry_after(str(e)) or backoff
            backoff = min(backoff * 2, 60)
            await log(card_id, f"    Rate limit exceeded. Sleeping {wait} seconds...")
            await asyncio.sleep(wait)


print("Loading cards from database...")
conn = sqlite3.connect("cards.db")
conn.row_factory = sqlite3.Row
with conn:
    cursor = conn.execute("SELECT * FROM cards")
    cards_rows = [dict(row) for row in cursor]

total_rows = len(cards_rows)
start_index = max(cli_args.start - 1, 0)
end_index = cli_args.end if cli_args.end is not None else total_rows
end_index = min(end_index, total_rows)

client = AsyncOpenAI()
CONCURRENCY = cli_args.workers
sem = asyncio.Semaphore(CONCURRENCY)


def _write_row(row: dict) -> None:
    with sqlite3.connect("cards.db") as save_conn:
        save_conn.execute(
            "UPDATE cards SET speaker_gender=? WHERE conjugation_id=?",
            (row.get("speaker_gender"), row["conjugation_id"]),
        )
        save_conn.commit()


async def save_row_to_db(row: dict) -> None:
    await asyncio.to_thread(_write_row, row)


prompt_template = """
Examine the following Spanish sentence and decide whether it forces the speaker's gender.

Sentence: "{sentence}"

Decision rules
• If the sentence requires masculine forms only → "male".
• If the sentence requires feminine forms only → "female".
• If both or neither are possible → "neutral".

Reply with exactly one of these JSON objects and nothing else:
    {{"speaker_gender":"neutral"}}
    {{"speaker_gender":"male"}}
    {{"speaker_gender":"female"}}
"""


async def process_card(card: dict) -> None:
    if not card.get("example_sentence") or card.get("speaker_gender"):
        return

    example_sentence = card["example_sentence"]
    await log(card["conjugation_id"], f"Processing example: {example_sentence}")

    prompt = prompt_template.format(sentence=example_sentence)

    try:
        response = await openai_chat_with_retry(
            card["conjugation_id"],
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a Spanish linguist."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        result = json.loads(response.choices[0].message.content)
        gender = result.get("speaker_gender")
        card["speaker_gender"] = gender
        await log(card["conjugation_id"], f"Detected gender: {gender}")
        await save_row_to_db(card)
    except Exception as exc:
        await log(card["conjugation_id"], f"    Error: {exc}")


async def main() -> None:
    tasks = [
        process_card(card)
        for card in cards_rows[start_index:end_index]
        if card.get("example_sentence") and not card.get("speaker_gender")
    ]
    await asyncio.gather(*tasks)

    await log("main", "\nSaving rows to cards.db...")
    with sqlite3.connect("cards.db") as save_conn:
        for row in cards_rows:
            save_conn.execute(
                "UPDATE cards SET speaker_gender=? WHERE conjugation_id=?",
                (row.get("speaker_gender"), row["conjugation_id"]),
            )
        save_conn.commit()

    total_processed = sum(
        1 for row in cards_rows[start_index:end_index] if row.get("example_sentence")
    )
    successful_rows = sum(
        1 for row in cards_rows[start_index:end_index] if row.get("speaker_gender")
    )
    await log("main", f"Rows examined: {total_processed}")
    await log("main", f"Speaker gender determined for: {successful_rows}")
    await log("main", "Done!")


if __name__ == "__main__":
    asyncio.run(main())
