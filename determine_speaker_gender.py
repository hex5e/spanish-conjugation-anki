#!/usr/bin/env python3
"""
Determine speaker gender from example sentences – o3 edition
------------------------------------------------------------
Key updates for reasoning models (o-series):

* MODEL = "o3"
* new CLI flag --effort {low,medium,high}  → maps to `reasoning_effort`
* still cap output with `max_completion_tokens`
* unchanged retry / DB logic
"""

import argparse
import asyncio
import json
import re
import sqlite3
from openai import AsyncOpenAI, RateLimitError  # ≥ 1.14.0

# --------------------------------------------------------------------------- #
# Model / token budget
MODEL = "o3"  # reasoning model
MAX_COMPLETION_TOKENS = (
    1024  # counts visible + reasoning tokens :contentReference[oaicite:0]{index=0}
)

# --------------------------------------------------------------------------- #
# CLI
parser = argparse.ArgumentParser(
    description="Determine speaker gender from example sentences (o3)"
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
parser.add_argument(
    "--effort",
    choices=["low", "medium", "high"],
    default="medium",
    help="Reasoning effort for o3 (low|medium|high)",
)
cli_args = parser.parse_args()

# --------------------------------------------------------------------------- #
print_lock = asyncio.Lock()


async def log(card_id: int | str, text: str) -> None:
    async with print_lock:
        print(f"[{card_id}] {text}", flush=True)


def parse_retry_after(message: str) -> float | None:
    """Extract 'Please try again in 20s' from RateLimitError text."""
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
            await log(card_id, f"    Rate limit exceeded. Sleeping {wait}s...")
            await asyncio.sleep(wait)


# --------------------------------------------------------------------------- #
print("Loading cards from database...")
conn = sqlite3.connect("cards.db")
conn.row_factory = sqlite3.Row
with conn:
    cards_rows = [dict(row) for row in conn.execute("SELECT * FROM cards")]

start_index = max(cli_args.start - 1, 0)
end_index = min(cli_args.end or len(cards_rows), len(cards_rows))

client = AsyncOpenAI()
sem = asyncio.Semaphore(cli_args.workers)


# --------------------------------------------------------------------------- #
def _write_row(row: dict) -> None:
    with sqlite3.connect("cards.db") as save_conn:
        save_conn.execute(
            "UPDATE cards SET speaker_gender=? WHERE conjugation_id=?",
            (row.get("speaker_gender"), row["conjugation_id"]),
        )
        save_conn.commit()


async def save_row_to_db(row: dict) -> None:
    await asyncio.to_thread(_write_row, row)


# --------------------------------------------------------------------------- #
PROMPT_TEMPLATE = """
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

    await log(card["conjugation_id"], f'Processing: "{card["example_sentence"]}"')

    prompt = PROMPT_TEMPLATE.format(sentence=card["example_sentence"])

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
            # NEW ⚙️  tell o3 how hard to think :contentReference[oaicite:1]{index=1}
            reasoning_effort=cli_args.effort,
        )
        gender = json.loads(response.choices[0].message.content).get("speaker_gender")
        card["speaker_gender"] = gender
        await log(card["conjugation_id"], f"Detected gender: {gender}")
        await save_row_to_db(card)

    except Exception as exc:
        await log(card["conjugation_id"], f"    Error: {exc}")


# --------------------------------------------------------------------------- #
async def main() -> None:
    tasks = [
        process_card(card)
        for card in cards_rows[start_index:end_index]
        if card.get("example_sentence") and not card.get("speaker_gender")
    ]
    await asyncio.gather(*tasks)

    await log("main", "\nSaving rows to cards.db...")

    total_examined = len(tasks)
    total_success = sum(
        1 for c in cards_rows[start_index:end_index] if c.get("speaker_gender")
    )
    await log("main", f"Rows examined: {total_examined}")
    await log("main", f"Speaker gender determined for: {total_success}")
    await log("main", "Done!")


if __name__ == "__main__":
    asyncio.run(main())
