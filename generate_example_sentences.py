import csv

row = 0

with open('cards.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)
    
    verb = rows[row]['verb']
    form = rows[row]['form']
    person = rows[row]['person']

with open('verbs.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)
    
    for row in rows:
        if row['verb'] == verb:
            verb_collocattions = row['verb_collocations']
            break

with open('forms.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

    for row in rows:
        if row['form'] == form:
            form_trigger_phrases = row['form_trigger_phrases']
            break

print("generating conjugation/example sentence...")
print(f"verb: {verb}")
print(f"form: {form}")
print(f"person: {person}")
print(f"verb collocations: {verb_collocattions}")
print(f"form trigger phrases: {form_trigger_phrases}")

