import sqlite3
import genanki
import random
import re
import os
import time
from datetime import datetime

# Add logging functionality
def log(message, level="INFO"):
    """Simple logging function with timestamps"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def main():
    start_time = time.time()
    log("Starting Spanish conjugation Anki deck generation")
    
    # Connect to database
    log("Connecting to database: cards.db")
    try:
        con = sqlite3.connect('cards.db')
        cards_cursor = con.cursor()
        log("Database connection successful")
    except Exception as e:
        log(f"Failed to connect to database: {e}", "ERROR")
        return
    
    # Define columns
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
    
    # Build and execute query
    select_clause = 'select ' + ', '.join(columns)
    where_clause = 'where ' + ' is not null and '.join(columns) + ' is not null'
    query = f"{select_clause} from cards {where_clause}"
    
    log("Executing database query...")
    log(f"Query: {query[:100]}...", "DEBUG")
    
    try:
        cards_cursor.execute(query)
        log("Query executed successfully")
    except Exception as e:
        log(f"Query failed: {e}", "ERROR")
        con.close()
        return
    
    # Fetch all rows
    log("Fetching rows from database...")
    rows = []
    rows_values = cards_cursor.fetchall()
    field_names = [value[0] for value in cards_cursor.description]
    
    log(f"Found {len(rows_values)} rows to process")
    
    # Convert rows to dictionaries
    log("Converting rows to dictionaries...")
    for i, row_values in enumerate(rows_values):
        if i % 1000 == 0 and i > 0:
            log(f"Processed {i}/{len(rows_values)} rows into dictionaries")
        
        row = {field_names[n]: row_values[n] for n in range(len(field_names))}
        rows.append(row)
    
    log(f"Converted all {len(rows)} rows to dictionaries")
    
    # Close database connection
    con.close()
    log("Database connection closed")
    
    # Create model and deck IDs
    model_id = random.randrange(1 << 30, 1 << 31)
    deck_id = random.randrange(1 << 30, 1 << 31)
    log(f"Generated model ID: {model_id}, deck ID: {deck_id}")
    
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
    
    # Create the cloze model
    log("Creating Anki cloze model...")
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
    
    log("Cloze model created successfully")
    
    # Create deck
    log("Creating Anki deck...")
    cloze_deck = genanki.Deck(
        deck_id,
        'Spanish Conjugations')
    log("Deck created successfully")
    
    # Initialize tracking variables
    problematic_rows = []
    cards_created = 0
    media_files = []
    missing_audio_files = []
    
    # Process rows
    log(f"Starting to process {len(rows)} rows into cards...")
    process_start_time = time.time()
    
    for i, row in enumerate(rows):
        if i % 100 == 0:
            elapsed = time.time() - process_start_time
            rate = i / elapsed if elapsed > 0 else 0
            eta = (len(rows) - i) / rate if rate > 0 else 0
            log(f"Progress: {i}/{len(rows)} cards ({i/len(rows)*100:.1f}%) - "
                f"Rate: {rate:.1f} cards/sec - ETA: {eta:.1f} seconds")
        
        try:
            conjugation = row['conjugation']
            example_sentence = row['example_sentence']
            
            # Create regex pattern
            pattern = r'\b' + re.escape(conjugation) + r'\b'
            matches = list(re.finditer(pattern, example_sentence, re.IGNORECASE))
            
            if len(matches) == 1:
                # Process successful match
                match = matches[0]
                matched_text = match.group()
                
                # Create hint text
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
                
                # Create cloze sentence
                start, end = match.span()
                cloze_sentence = (
                    example_sentence[:start] + 
                    f'{{{{c1::{matched_text}::{hint_text}}}}}' + 
                    example_sentence[end:]
                )
                
                # Build question content
                verb_info_parts = []
                verb_info_parts.append(f"<div class='verb-header'>{row['verb']}</div>")
                
                if person_map.get(row['person']):
                    verb_info_parts.append(f"<div class='person-info'>{person_map[row['person']]}</div>")
                
                form_display = form_display_map.get(row['form'], row['form'])
                verb_info_parts.append(f"<div class='form-info'>{form_display}</div>")
                
                text_field = ''.join(verb_info_parts) + cloze_sentence
                
                # Build extra info
                extra_parts = ['<div class="extra-info">']
                
                if row['regularity_class'] == 'regular':
                    regularity_html = '<span class="regular">regular</span> (hypothetical and real form are equivalent)'
                elif row['regularity_class'] == 'morphologically_irregular':
                    regularity_html = '<span class="morphologically">morphologically irregular</span> (form does not follow standard conjugation rules)'
                else:
                    regularity_html = '<span class="orthographically">orthographically irregular</span> (spoken word is regular, but spelling is irregular)'
                
                extra_parts.append(f"<strong>Hypothetical regular form:</strong> {row['hypothetical_regular_conjugation']}<br>")
                extra_parts.append(f"<strong>Regularity class:</strong> {regularity_html}<br>")
                extra_parts.append(f"<strong>Conjugation ID:</strong> {row['conjugation_id']}")
                
                # Handle audio
                if row.get('audio_path'):
                    audio_filename = row['audio_path'].replace('\\', '/')
                    audio_file_only = audio_filename.split('/')[-1]
                    extra_parts.append(f"<br><br>[sound:{audio_file_only}]")
                    media_files.append(row['audio_path'])
                
                extra_parts.append('<div class="contact-info">Any questions/problems/suggestions regarding this deck? You may reach out to the creator through hex5e@outlook.com</div>')
                extra_parts.append('</div>')
                
                extra_field = ''.join(extra_parts)
                
                # Create note with tags
                note = genanki.Note(
                    model=cloze_model,
                    fields=[text_field, extra_field])
                
                tags = []
                tags.append(f"verb::{row['verb']}")
                tags.append(f"form::{row['form']}")
                if row['person'] != 'not_applicable':
                    tags.append(f"person::{row['person']}")
                
                note.tags = tags
                cloze_deck.add_note(note)
                cards_created += 1
                
            else:
                # Log problematic row
                problematic_rows.append(row['conjugation_id'])
                if len(problematic_rows) <= 10:  # Only log first 10 to avoid spam
                    log(f"Problem with conjugation_id: {row['conjugation_id']} - "
                        f"'{conjugation}' appears {len(matches)} times", "WARNING")
                
        except Exception as e:
            log(f"Error processing row {i} (conjugation_id: {row.get('conjugation_id', 'unknown')}): {e}", "ERROR")
            problematic_rows.append(row.get('conjugation_id', f'row_{i}'))
    
    log(f"Card creation complete. Created {cards_created} cards, skipped {len(problematic_rows)} problematic rows")
    
    # Create package
    log("Creating Anki package...")
    package = genanki.Package(cloze_deck)
    
    # Add media files
    log(f"Adding {len(media_files)} media files to package...")
    media_added = 0
    
    for i, media_file in enumerate(media_files):
        if i % 100 == 0 and i > 0:
            log(f"Added {i}/{len(media_files)} media files")
        
        if os.path.exists(media_file):
            package.media_files.append(media_file)
            media_added += 1
        else:
            missing_audio_files.append(media_file)
            if len(missing_audio_files) <= 10:  # Only log first 10
                log(f"Audio file not found: {media_file}", "WARNING")
    
    log(f"Added {media_added} media files successfully, {len(missing_audio_files)} files missing")
    
    # Write package to file
    output_file = 'spanish_conjugation.apkg'
    log(f"Writing package to file: {output_file}")
    
    try:
        package.write_to_file(output_file)
        log(f"Successfully wrote package to {output_file}")
    except Exception as e:
        log(f"Failed to write package: {e}", "ERROR")
        return
    
    # Final summary
    elapsed_time = time.time() - start_time
    log("=" * 60)
    log("SUMMARY:")
    log(f"Total execution time: {elapsed_time:.2f} seconds")
    log(f"Cards created: {cards_created}")
    log(f"Problematic rows skipped: {len(problematic_rows)}")
    log(f"Media files added: {media_added}")
    log(f"Missing audio files: {len(missing_audio_files)}")
    log(f"Output file: {output_file}")
    log(f"Output file size: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")
    
    if problematic_rows and len(problematic_rows) <= 20:
        log(f"Problematic conjugation_ids: {problematic_rows}")
    elif problematic_rows:
        log(f"First 20 problematic conjugation_ids: {problematic_rows[:20]}")
        log(f"(and {len(problematic_rows) - 20} more...)")

if __name__ == "__main__":
    main()