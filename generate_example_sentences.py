from openai import OpenAI
import csv
import random
import json

model = "gpt-4.1-mini"
if model == "gpt-4.1":
    cards_update_column = "example_sentence_gpt4-1"
elif model == "gpt-4.1-mini":
    cards_update_column = "example_sentence_gpt4-1-mini"

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
    
    # Skip if already has content in the target column (optional)
    if card.get(cards_update_column):
        print(f"Skipping row {i+1}/{total_rows} - already has {cards_update_column}")
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
    
    # Sample collocations and trigger phrases
    selected_collocations = random.sample(verb_collocations, min(3, len(verb_collocations)))
    selected_trigger = random.sample(form_trigger_phrases, 1)
    
    prompt = f"""
You are given:
- verb: "{verb}"
- recommended collocations: {selected_collocations}
- form: "{form}"
- person: "{person}"
- form trigger phrases: {selected_trigger}


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
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"}
        )
        
        chat_response = json.loads(response.choices[0].message.content)
        
        # Update the row
        cards_rows[i]['conjugation'] = chat_response['conjugation']
        cards_rows[i][cards_update_column] = chat_response['example_sentence']
        
        print(f"  ✓ Generated: {chat_response['conjugation']} - {chat_response['example_sentence'][:50]}...")
        
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        continue
    
    # Optional: Save periodically (every 10 rows) to avoid losing progress
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

print("Done!")