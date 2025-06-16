from openai import OpenAI
import csv
import random
import json
import time
import re

# Configuration
MODEL = "gpt-4.1"  # Use "o3-mini" for faster processing
# REASONING_EFFORT = "medium"  # only used for reasoning models like o3-mini; Can be "low", "medium", or "high"
MAX_COMPLETION_TOKENS = 2048
# SEED = 42
FULL_AUTO_MODE = True  # Set to False to require pressing Enter after each conjugation
PERIODIC_SAVE_NUMBER = 1  # Save progress every N processed rows


def convert_to_array(string):
    """
    Convert a string representation of an array into an actual Python list
    Assumes string formatted like "[item1; item2; ...]"
    """
    items = string.strip("[]").split(";")
    array = [item.strip() for item in items]
    return array


# Read all CSV files once
print("Loading CSV files...")

# Read cards.csv
with open("cards.csv", mode="r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    cards_rows = list(reader)
    cards_fieldnames = reader.fieldnames

# Read verbs.csv and create a lookup dictionary
with open("verb_data/verbs.csv", mode="r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    verbs_dict = {row["verb"]: row["verb_collocations"] for row in reader}

# Read tenses.csv and create a lookup dictionary
with open("verb_data/tenses.csv", mode="r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    forms_dict = {row["form"]: row.get("form_trigger_phrases", "") for row in reader}

# Initialize OpenAI client once
client = OpenAI()

# Count rows that need processing
rows_to_process = sum(
    1
    for card in cards_rows
    if not card.get("example_sentence")
)
print(f"Found {rows_to_process} rows that need processing with {MODEL}")

# Process each row
total_rows = len(cards_rows)
processed_count = 0

for i, card in enumerate(cards_rows):
    verb = card["verb"]
    form = card["form"]
    person = card["person"]
    conjugation = card["conjugation"]

    # Skip if already has verified content
    if card.get("example_sentence"):
        continue

    processed_count += 1
    print(
        f"\nProcessing row {i+1}/{total_rows} (unfilled row {processed_count}/{rows_to_process}):"
    )
    print(f"  verb: {verb}")
    print(f"  form: {form}")
    print(f"  person: {person}")
    print(f"  conjugation: {conjugation}")

    # Get verb collocations
    verb_collocations = []
    if verb in verbs_dict and verbs_dict[verb]:
        verb_collocations = convert_to_array(verbs_dict[verb])

    # Get form trigger phrases
    form_trigger_phrases = []
    if form in forms_dict and forms_dict[form]:
        form_trigger_phrases = convert_to_array(forms_dict[form])

    # Skip if missing required data
    if not verb_collocations or not form_trigger_phrases:
        print(f"  Skipping - missing collocations or trigger phrases")
        continue

    # Prepare specifications
    imperativo_specification = (
        "Use exclamation marks; "
        if "imperativo" in form
        else "The sentence should NOT be a command; Do NOT use exclamation marks; "
    )

    # Initialize or update failure tracking
    if card.get("failure_counts"):
        failure_counts = json.loads(card["failure_counts"])
        failure_counts.pop("correct_conjugation", None)
    else:
        failure_counts = {
            "conjugation_in_sentence": 0,
            "grammar_ok": 0,
            "trigger_in_sentence": 0,
        }

    # Get existing attempt count or start fresh
    attempts = int(card.get("attempts_count", 0)) if card.get("attempts_count") else 0
    max_total_attempts = attempts + 3  # Allow 3 more attempts with o3
    success = False

    while attempts < max_total_attempts and not success:
        attempts += 1
        print(f"  Attempt {attempts} with {MODEL}...")

        # Sample collocations and trigger phrases
        selected_collocations = random.sample(
            verb_collocations, min(3, len(verb_collocations))
        )
        selected_trigger = random.sample(form_trigger_phrases, 1)[
            0
        ]  # Get the string, not list

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
            # Generate conjugation and sentence with o3
            response = client.chat.completions.create(
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
                # reasoning_effort=REASONING_EFFORT,
                # seed=SEED
            )

            generation_response = json.loads(response.choices[0].message.content)
            example_sentence = generation_response["example_sentence"]

            print(f"    Generated sentence: {example_sentence}...")

            # Check if the conjugation appears in the sentence (case-insensitive)
            conjugation_regex = re.compile(
                rf"\b{re.escape(conjugation)}\b", re.IGNORECASE
            )
            conjugation_in_sentence = bool(conjugation_regex.search(example_sentence))
            if not conjugation_in_sentence:
                failure_counts["conjugation_in_sentence"] += 1
                print("    \u2717 Failed: conjugation_in_sentence")

            # Verify the generation
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

            # Small delay to avoid rate limits
            time.sleep(2)

            # Verify with o3
            verification_response = client.chat.completions.create(
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
                # reasoning_effort=REASONING_EFFORT,
                # seed=SEED
            )

            verification_result = json.loads(
                verification_response.choices[0].message.content
            )

            # Check if all verifications passed
            all_passed = conjugation_in_sentence and all(verification_result.values())

            if all_passed:
                # Success! Update the row
                cards_rows[i]["example_sentence"] = example_sentence
                cards_rows[i]["attempts_count"] = str(attempts)
                cards_rows[i]["failure_counts"] = json.dumps(failure_counts)
                print(f"    ✓ All checks passed!")
                success = True
            else:
                # Track failures
                for check, passed in verification_result.items():
                    if not passed:
                        failure_counts[check] += 1
                        print(f"    ✗ Failed: {check}")

        except Exception as e:
            print(f"    ✗ Error: {str(e)}")
            continue

    # If we exhausted attempts without success
    if not success:
        cards_rows[i]["attempts_count"] = str(attempts)
        cards_rows[i]["failure_counts"] = json.dumps(failure_counts)
        print(f"  Failed after {attempts} attempts. Failures: {failure_counts}")

    # Interactive mode - wait for user to press Enter
    if not FULL_AUTO_MODE:
        input("\nPress Enter to continue to the next conjugation...")

    # Save periodically to avoid losing progress
    if processed_count % PERIODIC_SAVE_NUMBER == 0:
        print(f"\nSaving progress after processing {processed_count} unfilled rows...")
        with open("cards.csv", mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=cards_fieldnames, quoting=csv.QUOTE_MINIMAL
            )
            writer.writeheader()
            writer.writerows(cards_rows)

# Final save
print(f"\nSaving all {total_rows} rows to cards.csv...")
with open("cards.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(
        csvfile, fieldnames=cards_fieldnames, quoting=csv.QUOTE_MINIMAL
    )
    writer.writeheader()
    writer.writerows(cards_rows)

# Print summary statistics
successful_rows = sum(
    1 for row in cards_rows if row.get("example_sentence")
)
failed_rows = sum(
    1
    for row in cards_rows
    if row.get("attempts_count") and not row.get("example_sentence")
)

print("\n" + "=" * 50)
print("SUMMARY:")
print(f"Total rows in file: {total_rows}")
print(f"Rows processed this run: {processed_count}")
print(f"Total successful verifications: {successful_rows}")
print(f"Still failed after max attempts: {failed_rows}")

# Analyze failure patterns
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

print(f"\nDone!")
