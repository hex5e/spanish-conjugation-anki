import argparse
import asyncio
import random
import re
import sqlite3
from pathlib import Path
from openai import AsyncOpenAI, RateLimitError

MODEL = "gpt-4o-mini-tts"
INSTRUCTIONS = (
    "Acento: español de Colombia neutro. "
    "Tono: neutro. "
    "Velocidad: un 10 % más lenta de lo normal. "
    "Pronunciación: clara, marcando las consonantes."
)

VOICE_OPTIONS = {
    "male": ["ash", "onyx"],
    "female": ["coral", "shimmer"],
}


def choose_voice(gender: str | None) -> str:
    if gender == "male":
        return random.choice(VOICE_OPTIONS["male"])
    if gender == "female":
        return random.choice(VOICE_OPTIONS["female"])
    if gender == "neutral":
        gender = random.choice(["male", "female"])
        return choose_voice(gender)
    return random.choice(VOICE_OPTIONS["male"])


parser = argparse.ArgumentParser(description="Generate audio files")
parser.add_argument(
    "--start", type=int, default=1, help="1-indexed start row (inclusive)"
)
parser.add_argument(
    "--end", type=int, help="1-indexed end row (inclusive; defaults to all rows)"
)
parser.add_argument(
    "--workers", type=int, default=5, help="Number of concurrent requests"
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
sem = asyncio.Semaphore(cli_args.workers)


def _write_row(row: dict) -> None:
    with sqlite3.connect("cards.db") as save_conn:
        save_conn.execute(
            "UPDATE cards SET audio_path=? WHERE conjugation_id=?",
            (row.get("audio_path"), row["conjugation_id"]),
        )
        save_conn.commit()


async def save_row_to_db(row: dict) -> None:
    await asyncio.to_thread(_write_row, row)


async def process_card(card: dict) -> None:
    conjugation = card["conjugation"]
    audio_path = (
        Path("audio")
        / str(card["verb_id"])
        / str(card["form_id"])
        / str(card["person_id"])
        / f"{conjugation}.mp3"
    )

    if audio_path.exists():
        return

    audio_path.parent.mkdir(parents=True, exist_ok=True)
    voice = choose_voice(card.get("speaker_gender"))

    await log(card["conjugation_id"], f"Generating audio to {audio_path} using {voice}")

    backoff = 1.0
    while True:
        try:
            async with sem:
                async with client.audio.speech.with_streaming_response.create(
                    model=MODEL,
                    voice=voice,
                    input=conjugation,
                    instructions=INSTRUCTIONS,
                ) as response:
                    await response.stream_to_file(audio_path)
            card["audio_path"] = str(audio_path)
            await save_row_to_db(card)
            await log(card["conjugation_id"], "Audio saved")
            break
        except RateLimitError as e:
            wait = parse_retry_after(str(e)) or backoff
            backoff = min(backoff * 2, 60)
            await log(
                card["conjugation_id"], f"Rate limit exceeded. Sleeping {wait}s..."
            )
            await asyncio.sleep(wait)
        except Exception as exc:
            await log(card["conjugation_id"], f"Error: {exc}")
            break


async def main() -> None:
    tasks = [process_card(card) for card in cards_rows[start_index:end_index]]
    await asyncio.gather(*tasks)
    await log("main", "Done!")


if __name__ == "__main__":
    asyncio.run(main())
