from openai import OpenAI
import csv
import random
import json

cards_row = 0  # Change this to select a different card

model = "gpt-4.1"
if model == "gpt-4.1":
    cards_update_column = "example_sentence_gpt4-1"
elif model == "gpt-4.1-mini":
    cards_update_column = "example_sentence_gpt4-1-mini"

# ---------- Select card ------------------
def convert_to_array(string):
    """
    Convert a string representation of an array into an actual Python list
    Assumes string formatted like "[item1; item2; ...]"
    """
    items = string.strip('[]').split(';')
    array = [item.strip() for item in items]

    return array

with open('cards.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)
    
    verb = rows[cards_row]['verb']
    form = rows[cards_row]['form']
    person = rows[cards_row]['person']

with open('verbs.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)
    
    for row in rows:
        if row['verb'] == verb:
            verb_collocattions = row['verb_collocations']
            break

    verb_collocattions = convert_to_array(verb_collocattions)

with open('forms.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

    for row in rows:
        if row['form'] == form:
            form_trigger_phrases = row['form_trigger_phrases']
            break

    if form_trigger_phrases:
        form_trigger_phrases = convert_to_array(form_trigger_phrases)

# ---------- Generate example sentence ------------------
print("generating conjugation/example sentence...")
print(f"verb: {verb}")
print(f"form: {form}")
print(f"person: {person}")
print(f"verb collocations: {verb_collocattions}")
print(f"form trigger phrases: {form_trigger_phrases}")
print("\n\n")

reflexive_specification = "Include the reflexive pronoun in the conjugation; " if verb.endswith('se') else ""
imperativo_negativo_specification = "Include 'no' in the conjugation; " if form == "imperativo_negativo" else ""
imperativo_specification = "Use exclamation marks; " if "imperativo" in form else "The sentence should NOT be a command; Do NOT use exclamtion marks; "

prompt = f"""
You are given:
- verb: "{verb}"
- recommended collocations: {random.sample(verb_collocattions, 3)}
- form: "{form}"
- person: "{person}"
- form trigger phrases: {random.sample(form_trigger_phrases, 1)}


TASK
1. Create a JSON object with exactly two keys:
   • "conjugation" → the verb conjugated in the specified form. {reflexive_specification}{imperativo_negativo_specification}
   • "example_sentence" → one grammatically correct, context-appropriate sentence (Spanish). {imperativo_specification}
2. The sentence must include the conjugated verb, the form trigger phrase, and at least one recommended collocation. 
3. Output ONLY the JSON object—no markdown, comments, or extra text.

Example output
{{"conjugation":"hablo","example_sentence":"Yo hablo español con mis compañeros de trabajo todos los días."}}
"""

client = OpenAI() 

response = client.chat.completions.create(
    model=model,             # any chat-capable model works
    messages=[{"role": "user", "content": prompt}],
    temperature=0,
    response_format={"type": "json_object"}  # makes the model emit strict JSON
)

chat_response = json.loads(response.choices[0].message.content)

with open('cards.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)
    
    rows[cards_row]['conjugation'] = chat_response['conjugation']
    rows[cards_row][cards_update_column] = chat_response['example_sentence']
