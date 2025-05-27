from openai import OpenAI
import csv
import random
import json
import time

model = "o3-mini"  # Changed to o3

def convert_to_array(string):
    """
    Convert a string representation of an array into an actual Python list
    Assumes string formatted like "[item1; item2; ...]"
    """
    items = string.strip('[]').split(';')
    array = [item.strip() for item in items]
    return array

# Read all CSV files once
print("Loading CSV files...")

# Read cards.csv
with open('cards.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    cards_rows = list(reader)
    cards_fieldnames = reader.fieldnames

# Read verbs.csv and create a lookup dictionary
with open('verbs.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    verbs_dict = {row['verb']: row['verb_collocations'] for row in reader}

# Read forms.csv and create a lookup dictionary
with open('forms.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    forms_dict = {row['form']: row.get('form_trigger_phrases', '') for row in reader}

# Initialize OpenAI client once
client = OpenAI()

# Count rows that need processing
rows_to_process = sum(1 for card in cards_rows 
                     if not (card.get('conjugation_with_verification') and card.get('sentence_with_verification')))
print(f"Found {rows_to_process} rows that still need verification")

# Process each row
total_rows = len(cards_rows)
processed_count = 0

for i, card in enumerate(cards_rows):
    verb = card['verb']
    form = card['form']
    person = card['person']
    
    # Skip if already has verified content
    if card.get('conjugation_with_verification') and card.get('sentence_with_verification'):
        continue
    
    processed_count += 1
    print(f"\nProcessing row {i+1}/{total_rows} (unfilled row {processed_count}/{rows_to_process}):")
    print(f"  verb: {verb}")
    print(f"  form: {form}")
    print(f"  person: {person}")
    
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
    reflexive_specification = "Include the reflexive pronoun in the conjugation; " if verb.endswith('se') else ""
    imperativo_negativo_specification = "Include 'no' in the conjugation; " if form == "imperativo_negativo" else ""
    imperativo_specification = "Use exclamation marks; " if "imperativo" in form else "The sentence should NOT be a command; Do NOT use exclamation marks; "
    
    # Get existing attempts and failure counts
    existing_attempts = int(card.get('attempts_count', '0') or '0')
    existing_failures = json.loads(card.get('failure_counts', '{}') or '{}')
    
    # Initialize failure tracking with existing failures
    failure_counts = {
        "correct_conjugation": existing_failures.get("correct_conjugation", 0),
        "conjugation_in_sentence": existing_failures.get("conjugation_in_sentence", 0),
        "grammar_ok": existing_failures.get("grammar_ok", 0),
        "trigger_in_sentence": existing_failures.get("trigger_in_sentence", 0)
    }
    
    attempts = existing_attempts
    max_attempts = existing_attempts + 3  # Add 3 more attempts with o3
    success = False
    
    print(f"  Previous attempts: {existing_attempts}, trying {max_attempts - existing_attempts} more times with {model}")
    
    while attempts < max_attempts and not success:
        attempts += 1
        print(f"  Attempt {attempts} (attempt {attempts - existing_attempts} with {model})...")
        
        # Sample collocations and trigger phrases
        selected_collocations = random.sample(verb_collocations, min(3, len(verb_collocations)))
        selected_trigger = random.sample(form_trigger_phrases, 1)[0]  # Get the string, not list
        
        generation_prompt = f"""
You are given:
- verb: "{verb}"
- recommended collocations: {selected_collocations}
- form: "{form}"
- person: "{person}"
- form trigger phrases: [{selected_trigger}]


TASK
1. Create a JSON object with exactly two keys:
   • "conjugation" → the verb conjugated in the specified form. {reflexive_specification}{imperativo_negativo_specification}
   • "example_sentence" → one grammatically correct, context-appropriate sentence (Spanish). {imperativo_specification}
2. The sentence must include the conjugated verb, the form trigger phrase, and at least one recommended collocation. 
3. Output ONLY the JSON object—no markdown, comments, or extra text.

Example output
{{"conjugation":"hablo","example_sentence":"Yo hablo español con mis compañeros de trabajo todos los días."}}
"""
        
        try:
            # Generate conjugation and sentence
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": generation_prompt}],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            generation_response = json.loads(response.choices[0].message.content)
            conjugation = generation_response['conjugation']
            example_sentence = generation_response['example_sentence']
            
            print(f"    Generated: {conjugation} - {example_sentence[:50]}...")
            
            # Verify the generation
            verification_prompt = f"""
You are given
- verb: "{verb}"
- form: "{form}"
- person: "{person}"
- form_trigger_phrase: "{selected_trigger}"
- conjugation: "{conjugation}"
- example_sentence: "{example_sentence}"

TASK  
Return **only** a JSON object with four Boolean keys that independently signal whether each requirement below is satisfied (true / false).

Checks  
1. "correct_conjugation" - the supplied **conjugation** is the right form of **verb** for the specified **form** and **person**.  
   {reflexive_specification}{imperativo_specification}
2. "conjugation_in_sentence" - that exact **conjugation** string appears in **example_sentence**.
3. "grammar_ok" - **example_sentence** is grammatically correct Spanish.  
   {imperativo_negativo_specification}
4. "trigger_in_sentence" - **example_sentence** contains **form_trigger_phrase** (case-insensitive match is acceptable).

**Output format**
```json
{{
  "correct_conjugation": true,
  "conjugation_in_sentence": true,
  "grammar_ok": true,
  "trigger_in_sentence": true
}}
```
"""
            
            # Small delay to avoid rate limits
            time.sleep(0.5)
            
            # Verify
            verification_response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": verification_prompt}],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            verification_result = json.loads(verification_response.choices[0].message.content)
            
            # Check if all verifications passed
            all_passed = all(verification_result.values())
            
            if all_passed:
                # Success! Update the row
                cards_rows[i]['conjugation_with_verification'] = conjugation
                cards_rows[i]['sentence_with_verification'] = example_sentence
                cards_rows[i]['attempts_count'] = str(attempts)
                cards_rows[i]['failure_counts'] = json.dumps(failure_counts)
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
    
    # Update attempts and failure counts even if unsuccessful
    cards_rows[i]['attempts_count'] = str(attempts)
    cards_rows[i]['failure_counts'] = json.dumps(failure_counts)
    
    if not success:
        print(f"  Failed after {attempts} total attempts. Failures: {failure_counts}")
    
    # Save periodically (every 10 processed rows) to avoid losing progress
    if processed_count % 10 == 0:
        print(f"\nSaving progress after processing {processed_count} unfilled rows...")
        with open('cards.csv', mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cards_fieldnames, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            writer.writerows(cards_rows)

# Final save
print(f"\nSaving all {total_rows} rows to cards.csv...")
with open('cards.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=cards_fieldnames, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    writer.writerows(cards_rows)

# Print summary statistics
successful_rows = sum(1 for row in cards_rows if row.get('conjugation_with_verification'))
still_failed = sum(1 for row in cards_rows 
                  if row.get('attempts_count') and int(row.get('attempts_count', '0')) > 3 
                  and not row.get('conjugation_with_verification'))
newly_successful = processed_count - still_failed

print("\n" + "="*50)
print("SUMMARY:")
print(f"Total rows in file: {total_rows}")
print(f"Rows processed in this run: {processed_count}")
print(f"Newly successful with {model}: {newly_successful}")
print(f"Still failed after {model} attempts: {still_failed}")
print(f"Total successful rows: {successful_rows}")

# Analyze failure patterns for rows that still failed
if still_failed > 0:
    print(f"\nFailure analysis for {still_failed} rows that still failed:")
    total_failures = {"correct_conjugation": 0, "conjugation_in_sentence": 0, "grammar_ok": 0, "trigger_in_sentence": 0}
    
    for row in cards_rows:
        if (row.get('attempts_count') and int(row.get('attempts_count', '0')) > 3 
            and not row.get('conjugation_with_verification') 
            and row.get('failure_counts')):
            failures = json.loads(row['failure_counts'])
            for check, count in failures.items():
                total_failures[check] += count
    
    print("Total failures by check type:")
    for check, count in total_failures.items():
        print(f"  {check}: {count}")

print("\nDone!")