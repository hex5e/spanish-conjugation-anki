import asyncio
import re
from openai import AsyncOpenAI, RateLimitError
import argparse
import csv
import sqlite3
import random
import json

# Configuration
MODEL = "gpt-4.1"  # Use "o3-mini" for faster processing
# REASONING_EFFORT = "medium"  # only used for reasoning models like o3-mini; Can be "low", "medium", or "high"
MAX_COMPLETION_TOKENS = 2048
# SEED = 42
FULL_AUTO_MODE = True  # Set to False to require pressing Enter after each conjugation

parser = argparse.ArgumentParser(description="Generate example sentences")
parser.add_argument(
    "--start",
    type=int,
    default=1,
    help="1-indexed start row (inclusive)",
)
parser.add_argument(
    "--end",
    type=int,
    help="1-indexed end row (inclusive; defaults to all rows)",
)
parser.add_argument(
    "--workers",
    type=int,
    default=5,
    help="Number of concurrent OpenAI requests",
)
cli_args = parser.parse_args()


def convert_to_array(string):
    """
    Convert a string representation of an array into an actual Python list
    Assumes string formatted like "[item1; item2; ...]"
    """
    items = string.strip("[]").split(";")
    array = [item.strip() for item in items]
    return array


def parse_retry_after(message: str) -> float | None:
    """Extract retry wait time from an error message in seconds."""
    match = re.search(r"Please try again in (\d+)(ms|s)", message)
    if match:
        value = int(match.group(1))
        return value / 1000 if match.group(2) == "ms" else float(value)
    return None


async def openai_chat_with_retry(**kwargs):
    """Call OpenAI chat endpoint and retry when rate limited."""
    backoff = 1.0
    while True:
        try:
            async with sem:
                return await client.chat.completions.create(**kwargs)
        except RateLimitError as e:
            wait = parse_retry_after(str(e)) or backoff
            backoff = min(backoff * 2, 60)
            print(f"    Rate limit exceeded. Sleeping {wait} seconds...")
            await asyncio.sleep(wait)


# Read all CSV files once
print("Loading data files...")

# Read cards from SQLite database
conn = sqlite3.connect("cards.db")
conn.row_factory = sqlite3.Row
with conn:
    cursor = conn.execute("SELECT * FROM cards")
    cards_rows = [dict(row) for row in cursor]
    cards_fieldnames = [desc[0] for desc in cursor.description]

# Determine slice of rows to process
total_rows = len(cards_rows)
start_index = max(cli_args.start - 1, 0)
end_index = cli_args.end if cli_args.end is not None else total_rows
end_index = min(end_index, total_rows)

# Read verbs.csv and create a lookup dictionary
with open("verb_data/verbs.csv", mode="r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    verbs_dict = {row["verb"]: row["verb_collocations"] for row in reader}

# Read tenses.csv and create a lookup dictionary
with open("verb_data/tenses.csv", mode="r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    forms_dict = {row["form"]: row.get("form_trigger_phrases", "") for row in reader}

# Initialize OpenAI client once
client = AsyncOpenAI()
CONCURRENCY = cli_args.workers
sem = asyncio.Semaphore(CONCURRENCY)

# Count rows that need processing
rows_to_process = sum(
    1 for card in cards_rows[start_index:end_index] if not card.get("example_sentence")
)
selected_total = end_index - start_index
print(
    f"Found {rows_to_process} rows that need processing in {selected_total} selected rows with {MODEL}"
)


async def process_card(card):
    if card.get("example_sentence"):
        return

    verb = card["verb"]
    form = card["form"]
    person = card["person"]
    conjugation = card["conjugation"]

    print(f"\nProcessing row {card['conjugation_id']}/{total_rows}...")
    print(f"  verb: {verb}")
    print(f"  form: {form}")
    print(f"  person: {person}")
    print(f"  conjugation: {conjugation}")

    verb_collocations = []
    if verb in verbs_dict and verbs_dict[verb]:
        verb_collocations = convert_to_array(verbs_dict[verb])

    form_trigger_phrases = []
    if form in forms_dict and forms_dict[form]:
        form_trigger_phrases = convert_to_array(forms_dict[form])

    if not verb_collocations or not form_trigger_phrases:
        print("  Skipping - missing collocations or trigger phrases")
        return

    imperativo_specification = (
        "Use exclamation marks; "
        if "imperativo" in form
        else "The sentence should NOT be a command; Do NOT use exclamation marks; "
    )

    if card.get("failure_counts"):
        failure_counts = json.loads(card["failure_counts"])
        failure_counts.pop("correct_conjugation", None)
    else:
        failure_counts = {
            "conjugation_in_sentence": 0,
            "grammar_ok": 0,
            "trigger_in_sentence": 0,
        }

    attempts = int(card.get("attempts_count", 0)) if card.get("attempts_count") else 0
    max_total_attempts = attempts + 3
    success = False

    while attempts < max_total_attempts and not success:
        attempts += 1
        print(f"  Attempt {attempts} with {MODEL}...")

        selected_collocations = random.sample(
            verb_collocations, min(3, len(verb_collocations))
        )
        selected_trigger = random.sample(form_trigger_phrases, 1)[0]

        generation_prompt = f"""
You are given:
- verb: "{verb}"
- conjugation: "{conjugation}"
- recommended collocations: {selected_collocations}
- form: "{form}"
- form trigger: [{selected_trigger}]
- person: "{person}"


TASK
1. Create a JSON object with exactly one key:
   • "example_sentence" → one grammatically correct, context-appropriate sentence (Spanish). {imperativo_specification}
2. The sentence must include the provided conjugation, the form trigger phrase, and at least one recommended collocation.
3. Output ONLY the JSON object—no markdown, comments, or extra text.

Example output
{{"example_sentence":"Yo hablo español con mis compañeros de trabajo todos los días."}}
"""

        try:
            response = await openai_chat_with_retry(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Spanish-grammar assistant. "
                        "Follow the TASK strictly and output valid JSON only.",
                    },
                    {"role": "user", "content": generation_prompt},
                ],
                response_format={"type": "json_object"},
                max_completion_tokens=MAX_COMPLETION_TOKENS,
            )

            generation_response = json.loads(response.choices[0].message.content)
            example_sentence = generation_response["example_sentence"]

            print(f"    Generated sentence: {example_sentence}...")

            conjugation_regex = re.compile(
                rf"\b{re.escape(conjugation)}\b", re.IGNORECASE
            )
            conjugation_in_sentence = bool(conjugation_regex.search(example_sentence))
            if not conjugation_in_sentence:
                failure_counts["conjugation_in_sentence"] += 1
                print("    ✗ Failed: conjugation_in_sentence")

            verification_prompt = f"""
You are given
- verb: "{verb}"
- form: "{form}"
- person: "{person}"
- form_trigger: "{selected_trigger}"
- conjugation: "{conjugation}"
- example_sentence: "{example_sentence}"

TASK
Return **only** a JSON object with two Boolean keys that independently signal whether each requirement below is satisfied (true / false).

Checks
1. "grammar_ok" - **example_sentence** is grammatically correct Spanish.
2. "trigger_in_sentence" - **example_sentence** contains **form_trigger** (case-insensitive match is acceptable).

**Output format**
{{
  "grammar_ok": true,
  "trigger_in_sentence": true
}}
"""

            await asyncio.sleep(2)

            verification_response = await openai_chat_with_retry(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Spanish-grammar verification assistant. "
                        "Carefully check each requirement and output valid JSON only.",
                    },
                    {"role": "user", "content": verification_prompt},
                ],
                response_format={"type": "json_object"},
                max_completion_tokens=MAX_COMPLETION_TOKENS,
            )

            verification_result = json.loads(
                verification_response.choices[0].message.content
            )

            all_passed = conjugation_in_sentence and all(verification_result.values())

            if all_passed:
                card["example_sentence"] = example_sentence
                card["attempts_count"] = str(attempts)
                card["failure_counts"] = json.dumps(failure_counts)
                print("    ✓ All checks passed!")
                success = True
            else:
                for check, passed in verification_result.items():
                    if not passed:
                        failure_counts[check] += 1
                        print(f"    ✗ Failed: {check}")

        except Exception as e:
            print(f"    ✗ Error: {str(e)}")
            continue

    if not success:
        card["attempts_count"] = str(attempts)
        card["failure_counts"] = json.dumps(failure_counts)
        print(f"  Failed after {attempts} attempts. Failures: {failure_counts}")

    if not FULL_AUTO_MODE:
        await asyncio.to_thread(
            input, "\nPress Enter to continue to the next conjugation..."
        )


async def main():
    tasks = [
        process_card(card)
        for card in cards_rows[start_index:end_index]
        if not card.get("example_sentence")
    ]
    await asyncio.gather(*tasks)

    print(f"\nSaving rows to cards.db...")
    with sqlite3.connect("cards.db") as save_conn:
        for row in cards_rows:
            save_conn.execute(
                "UPDATE cards SET example_sentence=?, attempts_count=?, failure_counts=? WHERE conjugation_id=?",
                (
                    row.get("example_sentence"),
                    row.get("attempts_count"),
                    row.get("failure_counts"),
                    row["conjugation_id"],
                ),
            )
        save_conn.commit()

    successful_rows = sum(1 for row in cards_rows if row.get("example_sentence"))
    failed_rows = sum(
        1
        for row in cards_rows
        if row.get("attempts_count") and not row.get("example_sentence")
    )

    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Total rows in file: {total_rows}")
    print(f"Rows processed this run: {rows_to_process}")
    print(f"Total successful verifications: {successful_rows}")
    print(f"Still failed after max attempts: {failed_rows}")

    if failed_rows > 0:
        print("\nFailure analysis (all attempts including previous runs):")
        total_failures = {
            "conjugation_in_sentence": 0,
            "grammar_ok": 0,
            "trigger_in_sentence": 0,
        }

        for row in cards_rows:
            if row.get("failure_counts"):
                failures = json.loads(row["failure_counts"])
                for check, count in failures.items():
                    total_failures[check] += count

        print("Total failures by check type:")
        for check, count in total_failures.items():
            print(f"  {check}: {count}")

    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
