from openai import OpenAI
import csv
import random

cards_row = 0

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

prompt = (
    f"Generate a sentence using the verb '{verb}' in the form '{form}'. "
    f"Consider some of these common collocations when generating your sentence: {random.sample(verb_collocattions, 3)}. "
    "Make sure the sentence is grammatically correct and contextually appropriate."
)

print(f"Prompt: {prompt}")