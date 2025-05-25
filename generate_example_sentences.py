from openai import OpenAI
import csv
import random
import json
import time

model = "gpt-4.1"

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

# Process each row
total_rows = len(cards_rows)
for i, card in enumerate(cards_rows):
    verb = card['verb']
    form = card['form']
    person = card['person']
    
    # Skip if already has verified content
    if card.get('gpt_4_1_conjugation_with_verification') and card.get('gpt_4_1_sentence_with_verification'):
        print(f"Skipping row {i+1}/{total_rows} - already has verified content")
        continue
    
    print(f"\nProcessing row {i+1}/{total_rows}:")
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
    
    # Initialize failure tracking
    failure_counts = {
        "correct_conjugation": 0,
        "conjugation_in_sentence": 0,
        "grammar_ok": 0,
        "trigger_in_sentence": 0
    }
    
    attempts = 0
    max_attempts = 3
    success = False
    
    while attempts < max_attempts and not success:
        attempts += 1
        print(f"  Attempt {attempts}/{max_attempts}...")
        
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
            
            verify_reflexive_specification = "Include the reflexive pronoun in the conjugation; " if verb.endswith('se') else ""
            verify_imperativo_negativo_specification = "Include 'no' in the conjugation; " if form == "imperativo_negativo" else ""
            verify_imperativo_specification = "Use exclamation marks; " if "imperativo" in form else "The sentence should NOT be a command; Do NOT use exclamation marks; "

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
   {verify_reflexive_specification}{verify_imperativo_specification}
2. "conjugation_in_sentence" - that exact **conjugation** string appears in **example_sentence**.
3. "grammar_ok" - **example_sentence** is grammatically correct Spanish.  
   {verify_imperativo_negativo_specification}
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
                cards_rows[i]['gpt_4_1_conjugation_with_verification'] = conjugation
                cards_rows[i]['gpt_4_1_sentence_with_verification'] = example_sentence
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
    
    # If we exhausted attempts without success
    if not success:
        cards_rows[i]['attempts_count'] = str(attempts)
        cards_rows[i]['failure_counts'] = json.dumps(failure_counts)
        print(f"  Failed after {attempts} attempts. Failures: {failure_counts}")
    
    # Save periodically (every 10 rows) to avoid losing progress
    if (i + 1) % 10 == 0:
        print(f"\nSaving progress at row {i+1}...")
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
successful_rows = sum(1 for row in cards_rows if row.get('gpt_4_1_conjugation_with_verification'))
failed_rows = sum(1 for row in cards_rows if row.get('attempts_count') and not row.get('gpt_4_1_conjugation_with_verification'))

print("\n" + "="*50)
print("SUMMARY:")
print(f"Total rows processed: {total_rows}")
print(f"Successful verifications: {successful_rows}")
print(f"Failed after max attempts: {failed_rows}")

# Analyze failure patterns
if failed_rows > 0:
    print("\nFailure analysis:")
    total_failures = {"correct_conjugation": 0, "conjugation_in_sentence": 0, "grammar_ok": 0, "trigger_in_sentence": 0}
    
    for row in cards_rows:
        if row.get('failure_counts'):
            failures = json.loads(row['failure_counts'])
            for check, count in failures.items():
                total_failures[check] += count
    
    print("Total failures by check type:")
    for check, count in total_failures.items():
        print(f"  {check}: {count}")

print("\nDone!")