import sqlite3
import genanki
import random
import re

con = sqlite3.connect('cards.db')
cards_cursor = con.cursor()

# we will only create cards for rows in cards db that are filled in
columns = [
    'verb',
    'form',
    'person',
    'conjugation_id', 
    'conjugation', 
    'hypothetical_regular_conjugation',
    'regularity_class',
    'example_sentence',
    'audio_path'
    ]

select_clause = 'select ' + ', '.join(columns)
where_clause = 'where ' + ' is not null and '.join(columns) + ' is not null'

query = f"""
{select_clause}
from cards
{where_clause}
"""

cards_cursor.execute(query)

# rows will be a list of dictionaries
# for row in rows
#   row.keys() == cards column names
#   row.values() == value of column in that particular row
rows = []

rows_values = cards_cursor.fetchall()
field_names = [value[0] for value in cards_cursor.description]

for row_values in rows_values:
    row = {field_names[n]: row_values[n] for n in range(len(field_names))}

    rows.append(row)

"""
Example of what a row looks like

rows[10]
{
    'verb': 'ser',
    'form': 'indicativo_preterito',
    'person': '2nd_singular',
    'conjugation_id': '1_4_21',
    'conjugation': 'fuiste',
    'hypothetical_regular_conjugation': 'siste',
    'regularity_class': 'morphologically_irregular',
    'example_sentence': 'Ayer fuiste capaz de resolver el problema sin ayuda.',
    'audio_path': 'audio\\1\\4\\21\\fuiste.mp3'
}
"""

# Create a unique model ID for cloze cards
model_id = random.randrange(1 << 30, 1 << 31)

# Mapping dictionaries
regularity_class_map = {
    'regular': 'regular (hypothetical and real form are equivalent)',
    'morphologically_irregular': 'morphologically irregular (form does not follow standard conjugation rules)',
    'orthographically_irregular': 'orthographically irregular (spoken word is regular, but spelling is irregular)'
}

person_map = {
    'not_applicable': None,
    '1st_singular': 'yo',
    '2nd_singular': 'tú',
    '3rd_singular': 'él/ella',
    '1st_plural': 'nosotros',
    '2nd_plural': 'vosotros',
    '3rd_plural': 'ellos/ellas'
}

form_symbol_map = {
    'infinitivo': '',
    'gerundio': '',
    'participio': '',
    'indicativo_presente': '⊙⊙⊙',
    'indicativo_imperfecto': '⇠⇠⇠',
    'indicativo_preterito': '↧↧↧',
    'indicativo_futuro': '→→→',
    'condicional': '◇◇◇',
    'subjuntivo_presente': '∿∿∿',
    'subjuntivo_imperfecto': '↫↫↫',
    'subjuntivo_futuro': '↬↬↬',
    'imperativo_afirmativo': '!!!',
    'imperativo_negativo': '!!!'
}

form_display_map = {
    'infinitivo': 'infinitivo',
    'gerundio': 'gerundio',
    'participio': 'participio',
    'indicativo_presente': '⊙⊙⊙ indicativo presente ⊙⊙⊙',
    'indicativo_imperfecto': '⇠⇠⇠ indicativo imperfecto ⇠⇠⇠',
    'indicativo_preterito': '↧↧↧ indicativo pretérito ↧↧↧',
    'indicativo_futuro': '→→→ indicativo futuro →→→',
    'condicional': '◇◇◇ condicional ◇◇◇',
    'subjuntivo_presente': '∿∿∿ subjuntivo presente ∿∿∿',
    'subjuntivo_imperfecto': '↫↫↫ subjuntivo imperfecto ↫↫↫',
    'subjuntivo_futuro': '↬↬↬ subjuntivo futuro ↬↬↬',
    'imperativo_afirmativo': '!!! imperativo afirmativo !!!',
    'imperativo_negativo': '!!! imperativo negativo !!!'
}

# Define the cloze note model with custom styling
cloze_model = genanki.Model(
    model_id,
    'Spanish Conjugation Cloze Advanced',
    fields=[
        {'name': 'Text'},
        {'name': 'Extra'},
    ],
    templates=[
        {
            'name': 'Cloze',
            'qfmt': '''{{cloze:Text}}''',
            'afmt': '''{{cloze:Text}}<br><br>{{Extra}}''',
        },
    ],
    css='''
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 20px;
    text-align: center;
    color: #000;
    background-color: white;
}

.cloze {
    font-weight: bold;
    color: #0066cc;
}

.night_mode .card {
    color: #d0d0d0;
    background-color: #2f2f31;
}

.night_mode .cloze {
    color: #5599ff;
}

.extra-info {
    text-align: left;
    margin-top: 20px;
    font-size: 16px;
    line-height: 1.6;
}

.verb-header {
    font-size: 24px;
    margin-bottom: 5px;
}

.person-info {
    font-size: 18px;
    margin-bottom: 5px;
}

.form-info {
    font-size: 16px;
    color: #666;
    margin-bottom: 20px;
}

.night_mode .form-info {
    color: #999;
}

.regular {
    color: #28a745;
    font-weight: bold;
}

.morphologically {
    color: #dc3545;
    font-weight: bold;
}

.orthographically {
    color: #ffc107;
    font-weight: bold;
}

.contact-info {
    margin-top: 20px;
    font-size: 14px;
    color: #666;
    font-style: italic;
}

.night_mode .contact-info {
    color: #999;
}
''',
    model_type=genanki.Model.CLOZE)

# Create a deck with a unique ID
deck_id = random.randrange(1 << 30, 1 << 31)
cloze_deck = genanki.Deck(
    deck_id,
    'Spanish Conjugations - Advanced Cloze')

# Track problematic rows and media files
problematic_rows = []
cards_created = 0
media_files = []

# Create cloze notes from your rows data
for row in rows:
    conjugation = row['conjugation']
    example_sentence = row['example_sentence']
    
    # Create a regex pattern that matches the conjugation as a whole word (case-insensitive)
    pattern = r'\b' + re.escape(conjugation) + r'\b'
    
    # Find all matches (case-insensitive)
    matches = list(re.finditer(pattern, example_sentence, re.IGNORECASE))
    
    if len(matches) == 1:
        # Get the actual matched text (preserves original case)
        match = matches[0]
        matched_text = match.group()
        
        # Create the hint text with proper formatting
        person_text = person_map.get(row['person'], '')
        form_symbol = form_symbol_map.get(row['form'], '')
        
        if person_text and form_symbol:
            hint_text = f"{form_symbol}...{person_text}...{row['verb']}...{person_text}...{form_symbol}"
        elif person_text:
            hint_text = f"{person_text}...{row['verb']}...{person_text}"
        elif form_symbol:
            hint_text = f"{form_symbol}...{row['verb']}...{form_symbol}"
        else:
            hint_text = f"{row['verb']}"
        
        # Replace only the matched occurrence with cloze syntax
        start, end = match.span()
        cloze_sentence = (
            example_sentence[:start] + 
            f'{{{{c1::{matched_text}::{hint_text}}}}}' + 
            example_sentence[end:]
        )
        
        # Build the question content
        verb_info_parts = []
        verb_info_parts.append(f"<div class='verb-header'>{row['verb']}</div>")
        
        if person_map.get(row['person']):
            verb_info_parts.append(f"<div class='person-info'>{person_map[row['person']]}</div>")
        
        form_display = form_display_map.get(row['form'], row['form'])
        verb_info_parts.append(f"<div class='form-info'>{form_display}</div>")
        
        # Combine with cloze sentence
        text_field = ''.join(verb_info_parts) + cloze_sentence
        
        # Build extra info for answer
        extra_parts = ['<div class="extra-info">']
        
        # Determine regularity class for coloring
        if row['regularity_class'] == 'regular':
            regularity_html = '<span class="regular">regular</span> (hypothetical and real form are equivalent)'
        elif row['regularity_class'] == 'morphologically_irregular':
            regularity_html = '<span class="morphologically">morphologically irregular</span> (form does not follow standard conjugation rules)'
        else:  # orthographically_irregular
            regularity_html = '<span class="orthographically">orthographically irregular</span> (spoken word is regular, but spelling is irregular)'
        
        extra_parts.append(f"<strong>Hypothetical regular form:</strong> {row['hypothetical_regular_conjugation']}<br>")
        extra_parts.append(f"<strong>Regularity class:</strong> {regularity_html}<br>")
        extra_parts.append(f"<strong>Conjugation ID:</strong> {row['conjugation_id']}")
        
        # Add audio if available
        if row.get('audio_path'):
            # Convert Windows path to forward slashes for Anki
            audio_filename = row['audio_path'].replace('\\', '/')
            # Extract just the filename for the sound tag
            audio_file_only = audio_filename.split('/')[-1]
            extra_parts.append(f"<br><br>[sound:{audio_file_only}]")
            media_files.append(row['audio_path'])
        
        extra_parts.append('<div class="contact-info">Any questions/problems/suggestions regarding this deck? You may reach out to the creator through hex5e@outlook.com</div>')
        extra_parts.append('</div>')
        
        extra_field = ''.join(extra_parts)
        
        # Create the note
        note = genanki.Note(
            model=cloze_model,
            fields=[text_field, extra_field])
        cloze_deck.add_note(note)
        cards_created += 1
    else:
        # Log problematic row
        problematic_rows.append(row['conjugation_id'])
        print(f"Problem with conjugation_id: {row['conjugation_id']}")
        print(f"  Conjugation '{conjugation}' appears {len(matches)} times in: {example_sentence}")
        if matches:
            print(f"  Found at: {[match.group() for match in matches]}")
        print()

# Create package with media files
package = genanki.Package(cloze_deck)

# Add media files to the package
import os
for media_file in media_files:
    if os.path.exists(media_file):
        package.media_files.append(media_file)
    else:
        print(f"Warning: Audio file not found: {media_file}")

# Write the package to a file
package.write_to_file('spanish_conjugations_advanced_cloze.apkg')

print(f"\nCreated Anki cloze deck with {cards_created} cards!")
print(f"Skipped {len(problematic_rows)} problematic rows")
if problematic_rows:
    print(f"Problematic conjugation_ids: {problematic_rows}")
print(f"Added {len(media_files)} audio files to the deck")
print("The deck has been saved as 'spanish_conjugations_advanced_cloze.apkg'")