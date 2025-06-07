import csv
import os

def load_csv_data(filename, id_column, value_column):
    """Load data from CSV file and return as list of tuples"""
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((int(row[id_column]), row[value_column]))
    return data

def get_verb_stem_and_ending(verb):
    """Extract the stem and ending from a verb"""
    if verb.endswith('se'):
        # For reflexive verbs, remove 'se' first
        base_verb = verb[:-2]
        if base_verb.endswith('ar'):
            return base_verb[:-2], 'ar', True
        elif base_verb.endswith('er'):
            return base_verb[:-2], 'er', True
        elif base_verb.endswith('ir') or base_verb.endswith('ír'):
            return base_verb[:-2], 'ir', True
        else:
            return base_verb, '', True
    
    # Handle non-reflexive verbs
    if verb.endswith('ar'):
        return verb[:-2], 'ar', False
    elif verb.endswith('er'):
        return verb[:-2], 'er', False
    elif verb.endswith('ir') or verb.endswith('ír'):
        return verb[:-2], 'ir', False
    else:
        return verb, '', False

def get_reflexive_pronoun(person_id):
    """Get the appropriate reflexive pronoun for a given person"""
    pronouns = {
        11: 'me',    # yo
        21: 'te',    # tú
        31: 'se',    # él/ella/usted
        12: 'nos',   # nosotros
        22: 'os',    # vosotros
        32: 'se'     # ellos/ellas/ustedes
    }
    return pronouns.get(person_id, '')

def conjugate_regular(verb, form_id, person_id):
    """Generate regular conjugation for a given verb, form, and person"""
    stem, ending, is_reflexive = get_verb_stem_and_ending(verb)
    
    # Handle non-conjugated forms
    if form_id == 0:  # infinitivo
        return verb
    elif form_id == 1:  # gerundio
        base_form = ''
        if ending == 'ar':
            base_form = stem + 'ando'
        else:  # -er, -ir
            base_form = stem + 'iendo'

        # For reflexive verbs, attach pronoun to the end of gerundio
        if is_reflexive:
            if base_form.endswith('ando'):
                return base_form.replace('ando', 'ándose')
            elif base_form.endswith('iendo'):
                return base_form.replace('iendo', 'iéndose')
            elif base_form.endswith('yendo'):
                return base_form.replace('yendo', 'yéndose')
            return base_form + 'se'
        return base_form
        
    elif form_id == 2:  # participio
        if is_reflexive:
            return ''  # Reflexive verbs don't have participio
        if ending == 'ar':
            return stem + 'ado'
        else:  # -er, -ir
            return stem + 'ido'
    
    # Handle person_id 0 (not_applicable)
    if person_id == 0:
        return ''
    
    # Regular conjugation patterns for each form and ending
    conjugations = {
        # indicativo_presente
        3: {
            'ar': {11: 'o', 21: 'as', 31: 'a', 12: 'amos', 22: 'áis', 32: 'an'},
            'er': {11: 'o', 21: 'es', 31: 'e', 12: 'emos', 22: 'éis', 32: 'en'},
            'ir': {11: 'o', 21: 'es', 31: 'e', 12: 'imos', 22: 'ís', 32: 'en'}
        },
        # indicativo_preterito
        4: {
            'ar': {11: 'é', 21: 'aste', 31: 'ó', 12: 'amos', 22: 'asteis', 32: 'aron'},
            'er': {11: 'í', 21: 'iste', 31: 'ió', 12: 'imos', 22: 'isteis', 32: 'ieron'},
            'ir': {11: 'í', 21: 'iste', 31: 'ió', 12: 'imos', 22: 'isteis', 32: 'ieron'}
        },
        # indicativo_imperfecto
        5: {
            'ar': {11: 'aba', 21: 'abas', 31: 'aba', 12: 'ábamos', 22: 'abais', 32: 'aban'},
            'er': {11: 'ía', 21: 'ías', 31: 'ía', 12: 'íamos', 22: 'íais', 32: 'ían'},
            'ir': {11: 'ía', 21: 'ías', 31: 'ía', 12: 'íamos', 22: 'íais', 32: 'ían'}
        },
        # indicativo_futuro
        6: {
            'ar': {11: 'aré', 21: 'arás', 31: 'ará', 12: 'aremos', 22: 'aréis', 32: 'arán'},
            'er': {11: 'eré', 21: 'erás', 31: 'erá', 12: 'eremos', 22: 'eréis', 32: 'erán'},
            'ir': {11: 'iré', 21: 'irás', 31: 'irá', 12: 'iremos', 22: 'iréis', 32: 'irán'}
        },
        # condicional
        7: {
            'ar': {11: 'aría', 21: 'arías', 31: 'aría', 12: 'aríamos', 22: 'aríais', 32: 'arían'},
            'er': {11: 'ería', 21: 'erías', 31: 'ería', 12: 'eríamos', 22: 'eríais', 32: 'erían'},
            'ir': {11: 'iría', 21: 'irías', 31: 'iría', 12: 'iríamos', 22: 'iríais', 32: 'irían'}
        },
        # subjuntivo_presente
        8: {
            'ar': {11: 'e', 21: 'es', 31: 'e', 12: 'emos', 22: 'éis', 32: 'en'},
            'er': {11: 'a', 21: 'as', 31: 'a', 12: 'amos', 22: 'áis', 32: 'an'},
            'ir': {11: 'a', 21: 'as', 31: 'a', 12: 'amos', 22: 'áis', 32: 'an'}
        },
        # subjuntivo_imperfecto (two forms, using -ra form)
        9: {
            'ar': {11: 'ara', 21: 'aras', 31: 'ara', 12: 'áramos', 22: 'arais', 32: 'aran'},
            'er': {11: 'iera', 21: 'ieras', 31: 'iera', 12: 'iéramos', 22: 'ierais', 32: 'ieran'},
            'ir': {11: 'iera', 21: 'ieras', 31: 'iera', 12: 'iéramos', 22: 'ierais', 32: 'ieran'}
        },
        # subjuntivo_futuro
        10: {
            'ar': {11: 'are', 21: 'ares', 31: 'are', 12: 'áremos', 22: 'areis', 32: 'aren'},
            'er': {11: 'iere', 21: 'ieres', 31: 'iere', 12: 'iéremos', 22: 'iereis', 32: 'ieren'},
            'ir': {11: 'iere', 21: 'ieres', 31: 'iere', 12: 'iéremos', 22: 'iereis', 32: 'ieren'}
        },
        # imperativo_affirmativo
        11: {
            'ar': {21: 'a', 31: 'e', 12: 'emos', 22: 'ad', 32: 'en'},
            'er': {21: 'e', 31: 'a', 12: 'amos', 22: 'ed', 32: 'an'},
            'ir': {21: 'e', 31: 'a', 12: 'amos', 22: 'id', 32: 'an'}
        },
        # imperativo_negativo
        12: {
            'ar': {21: 'es', 31: 'e', 12: 'emos', 22: 'éis', 32: 'en'},
            'er': {21: 'as', 31: 'a', 12: 'amos', 22: 'áis', 32: 'an'},
            'ir': {21: 'as', 31: 'a', 12: 'amos', 22: 'áis', 32: 'an'}
        }
    }
    
    # For future and conditional, use the full infinitive as the stem
    if form_id in [6, 7]:
        if is_reflexive:
            base_verb = verb[:-2]  # Remove 'se'
        else:
            base_verb = verb
        
        if form_id == 6:  # futuro
            endings = {11: 'é', 21: 'ás', 31: 'á', 12: 'emos', 22: 'éis', 32: 'án'}
        else:  # condicional
            endings = {11: 'ía', 21: 'ías', 31: 'ía', 12: 'íamos', 22: 'íais', 32: 'ían'}
        
        if person_id in endings:
            conjugated = base_verb + endings[person_id]
            if is_reflexive:
                pronoun = get_reflexive_pronoun(person_id)
                return pronoun + ' ' + conjugated
            return conjugated
    
    # Get the appropriate conjugation
    if form_id in conjugations and ending in conjugations[form_id]:
        if person_id in conjugations[form_id][ending]:
            base_conjugation = stem + conjugations[form_id][ending][person_id]
            
            # Handle reflexive pronouns and special forms
            if is_reflexive:
                pronoun = get_reflexive_pronoun(person_id)
                if form_id == 11:  # imperativo afirmativo - pronoun attached to end
                    # Special handling for 2nd plural - drop the trailing 'd'
                    if person_id == 22 and base_conjugation.endswith('d'):
                        trimmed = base_conjugation[:-1]
                        if verb.rstrip('se') == 'ir':
                            return 'idos'
                        if ending == 'ir' and trimmed.endswith('i'):
                            trimmed = trimmed[:-1] + 'í'
                        return trimmed + pronoun
                    return base_conjugation + pronoun
                else:  # All other forms - pronoun before verb
                    result = pronoun + ' ' + base_conjugation
                    if form_id == 12:  # imperativo negativo - add 'no' at beginning
                        return 'no ' + result
                    return result
            else:
                # Non-reflexive imperativo negativo - just add 'no'
                if form_id == 12:
                    return 'no ' + base_conjugation
                return base_conjugation
    
    return ''

def generate_conjugation_table():
    """Generate the main conjugation table"""
    # Try to load from CSV files first
    try:
        verbs = load_csv_data('verbs.csv', 'verb_id', 'verb')
        forms = load_csv_data('forms.csv', 'form_id', 'form')
        persons = load_csv_data('persons.csv', 'person_id', 'person')
        print("Loaded data from existing CSV files")
    except FileNotFoundError:
        print("CSV files not found.")
        return
    
    # Generate the conjugation table
    conjugation_table = []
    
    for verb_id, verb in verbs:
        for form_id, form in forms:
            # Skip participio for reflexive verbs
            if form_id == 2 and verb.endswith('se'):
                continue
                
            # Determine which persons apply to this form
            if form_id <= 2:  # infinitivo, gerundio, participio
                applicable_persons = [(0, "not_applicable")]
            elif form_id in [11, 12]:  # imperativo forms - no 1st person singular
                applicable_persons = persons[2:]  # Skip "not_applicable" and "1st_singular"
            else:  # All other forms use the 6 person conjugations
                applicable_persons = persons[1:]  # Skip the first "not_applicable"
            
            for person_id, person in applicable_persons:
                # Generate hypothetical regular conjugation
                regular_conjugation = conjugate_regular(verb, form_id, person_id)
                
                row = {
                    'verb_id': verb_id,
                    'verb': verb,
                    'form_id': form_id,
                    'form': form,
                    'person_id': person_id,
                    'person': person,
                    'conjugation_id': f"{verb_id}_{form_id}_{person_id}",
                    'hypothetical_regular_conjugation': regular_conjugation,
                    'conjugation': '',  # Left blank as requested
                    'example_sentence_gpt4-1': '',  # Left blank for GPT-4 examples
                    'example_sentence_gpt4-1-mini': '',  # Left blank for GPT-4 mini examples
                    'gpt_4_1_conjugation_with_verification': '',  # New verification column
                    'gpt_4_1_sentence_with_verification': '',  # New verification column
                    'attempts_count': '',  # Track number of attempts
                    'failure_counts': ''  # Track which checks failed
                }
                conjugation_table.append(row)
    
    # Write to CSV file
    output_filename = 'cards.csv'
    fieldnames = ['verb_id', 'verb', 'form_id', 'form', 'person_id', 'person', 
                  'conjugation_id', 'hypothetical_regular_conjugation', 'conjugation', 
                  'example_sentence_gpt4-1', 'example_sentence_gpt4-1-mini',
                  'gpt_4_1_conjugation_with_verification', 'gpt_4_1_sentence_with_verification',
                  'attempts_count', 'failure_counts']
    
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(conjugation_table)
    
    # Calculate statistics
    reflexive_count = sum(1 for _, verb in verbs if verb.endswith('se'))
    non_reflexive_count = len(verbs) - reflexive_count
    
    print(f"\nSuccessfully generated {output_filename}")
    print(f"Total rows: {len(conjugation_table)}")
    print(f"\nBreakdown:")
    print(f"- Total verbs: {len(verbs)}")
    print(f"  - Non-reflexive verbs: {non_reflexive_count}")
    print(f"  - Reflexive verbs: {reflexive_count}")
    
    # Show sample rows with regular conjugations
    print("\nSample rows with hypothetical regular conjugations:")
    print("-" * 130)
    print("verb_id | verb       | form                | person       | conjugation_id | hypothetical_regular")
    print("-" * 130)
    
    # Show specific examples
    examples = [
        ('hablar', 'indicativo_presente', '1st_singular'),
        ('hablar', 'imperativo_negativo', '2nd_singular'),
        ('levantarse', 'indicativo_presente', '1st_singular'),
        ('levantarse', 'gerundio', 'not_applicable'),
        ('levantarse', 'imperativo_affirmativo', '2nd_singular'),
        ('levantarse', 'imperativo_negativo', '2nd_singular'),
        ('ducharse', 'indicativo_futuro', '3rd_plural')
    ]
    
    for verb_name, form_name, person_name in examples:
        for row in conjugation_table:
            if row['verb'] == verb_name and row['form'] == form_name and row['person'] == person_name:
                print(f"{row['verb_id']:7} | {row['verb']:10} | {row['form']:19} | {row['person']:12} | "
                      f"{row['conjugation_id']:14} | {row['hypothetical_regular_conjugation']}")
                break

if __name__ == "__main__":
    generate_conjugation_table()