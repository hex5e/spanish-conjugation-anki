import csv
import sqlite3
from pathlib import Path

from utilities.regular_form_generator import RegularFormGenerator
from utilities.conjugation_regularity_classifier import (
    ConjugationRegularityClassifier,
)
from utilities.get_conjugation_rae import (
    RAEConjugationFetcher,
    RAEConjugationTransformer,
    strip_reflexive,
)

# instantiate a single generator for regular forms
generator = RegularFormGenerator()
classifier = ConjugationRegularityClassifier()

verbs_dictionary_conjugations = {}

# Columns for the output CSV
FIELDNAMES = [
    "verb_id",
    "verb",
    "form_id",
    "form",
    "person_id",
    "person",
    "conjugation_id",
    "hypothetical_regular_conjugation",
    "conjugation",
    "regularity_class",
    "example_sentence",
    "attempts_count",
    "failure_counts",
]


def make_row(**kwargs) -> dict:
    """Return a row dict with default blank values and overrides."""
    row = {k: "" for k in FIELDNAMES}
    row.update(kwargs)
    return row


# verbs that lack an imperative
NO_IMPERATIVE_VERBS = {
    "deber",
    "delinquir",
    "gustar",
    "haber",
    "nacer",
    "ocurrir",
    "poder",
    "soler",
    "parecer",
    "resultar",
    "valer",
    "caber",
    "yacer",
    "existir",
    "necesitar",
}

# verbs that only use third-person forms
THIRD_PERSON_ONLY_VERBS = {"gustar", "ocurrir", "resultar", "existir"}

# verbs restricted to certain forms
SOLER_ALLOWED_FORMS = {3, 5}  # indicativo_presente and indicativo_imperfecto


def load_csv_data(filename, id_column, value_column):
    """Load data from CSV file and return as list of tuples"""
    data = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((int(row[id_column]), row[value_column]))
    return data


def generate_conjugation_table():
    """Generate the main conjugation table"""
    # Try to load from CSV files first
    try:
        verbs = load_csv_data(Path("verb_data") / "verbs.csv", "verb_id", "verb")
        forms = load_csv_data(Path("verb_data") / "tenses.csv", "form_id", "form")
        persons = load_csv_data(
            Path("verb_data") / "persons.csv", "person_id", "person"
        )
        print("Loaded data from existing CSV files")
    except FileNotFoundError:
        print("CSV files not found.")
        return

    # Populate verbs_dictionary_conjugations using the RAE crawler
    fetcher = RAEConjugationFetcher()
    for _, verb in verbs:
        base, is_reflexive = strip_reflexive(verb)
        try:
            raw = fetcher.get_conjugation(base)
            transformer = RAEConjugationTransformer(verb, is_reflexive=is_reflexive)
            verbs_dictionary_conjugations[verb] = transformer.transform(raw)
        except Exception as exc:  # pragma: no cover - network call
            raise RuntimeError(f"Failed to fetch conjugations for {verb}") from exc

    # Generate the conjugation table
    conjugation_table = []

    for verb_id, verb in verbs:
        for form_id, form in forms:
            # Skip participio for reflexive verbs
            if form_id == 2 and verb.endswith("se"):
                continue

            # Skip imperatives for verbs without that form
            if form_id in [11, 12] and verb in NO_IMPERATIVE_VERBS:
                continue

            # Skip the imperfect past of "nacer"
            if verb == "nacer" and form_id == 5:
                continue

            # Limit "soler" to present and imperfect
            if verb == "soler" and form_id not in SOLER_ALLOWED_FORMS:
                continue

            # Determine which persons apply to this form
            if form_id <= 2:  # infinitivo, gerundio, participio
                applicable_persons = [(0, "not_applicable")]
            elif form_id in [11, 12]:  # imperativo forms - no 1st person singular
                applicable_persons = persons[
                    2:
                ]  # Skip "not_applicable" and "1st_singular"
            else:  # All other forms use the 6 person conjugations
                applicable_persons = persons[1:]  # Skip the first "not_applicable"

            # Remove 1st and 2nd persons for certain verbs
            if verb in THIRD_PERSON_ONLY_VERBS:
                applicable_persons = [
                    p for p in applicable_persons if p[0] in {0, 31, 32}
                ]

            for person_id, person in applicable_persons:
                # Generate hypothetical regular conjugation
                regular_conjugation = generator.generate(verb, form, person)

                # Look up the real conjugation from the scraped data
                form_map = verbs_dictionary_conjugations.get(verb, {}).get(form)
                if isinstance(form_map, dict):
                    conjugation = form_map.get(person, "")
                else:
                    conjugation = form_map if person == "not_applicable" else ""

                row = make_row(
                    verb_id=verb_id,
                    verb=verb,
                    form_id=form_id,
                    form=form,
                    person_id=person_id,
                    person=person,
                    conjugation_id=f"{verb_id}_{form_id}_{person_id}",
                    hypothetical_regular_conjugation=regular_conjugation,
                    conjugation=conjugation,
                    regularity_class=classifier.classify(
                        verb, {form: {person: conjugation}}
                    ),
                )
                conjugation_table.append(row)

    # Write to SQLite database
    output_filename = "cards.db"

    conn = sqlite3.connect(output_filename)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS cards")
    cur.execute(
        """
        CREATE TABLE cards (
            verb_id INTEGER,
            verb TEXT,
            form_id INTEGER,
            form TEXT,
            person_id INTEGER,
            person TEXT,
            conjugation_id TEXT PRIMARY KEY,
            hypothetical_regular_conjugation TEXT,
            conjugation TEXT,
            regularity_class TEXT,
            example_sentence TEXT,
            attempts_count INTEGER,
            failure_counts TEXT
        )
        """
    )
    cur.executemany(
        "INSERT INTO cards VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [
            (
                row["verb_id"],
                row["verb"],
                row["form_id"],
                row["form"],
                row["person_id"],
                row["person"],
                row["conjugation_id"],
                row["hypothetical_regular_conjugation"],
                row["conjugation"],
                row["regularity_class"],
                row["example_sentence"],
                row["attempts_count"],
                row["failure_counts"],
            )
            for row in conjugation_table
        ],
    )
    conn.commit()
    conn.close()

    # Calculate statistics
    reflexive_count = sum(1 for _, verb in verbs if verb.endswith("se"))
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
    print(
        "verb_id | verb       | form                | person       | conjugation_id | hypothetical_regular"
    )
    print("-" * 130)

    # Show specific examples
    examples = [
        ("hablar", "indicativo_presente", "1st_singular"),
        ("hablar", "imperativo_negativo", "2nd_singular"),
        ("levantarse", "indicativo_presente", "1st_singular"),
        ("levantarse", "gerundio", "not_applicable"),
        ("levantarse", "imperativo_afirmativo", "2nd_singular"),
        ("levantarse", "imperativo_negativo", "2nd_singular"),
        ("ducharse", "indicativo_futuro", "3rd_plural"),
    ]

    for verb_name, form_name, person_name in examples:
        for row in conjugation_table:
            if (
                row["verb"] == verb_name
                and row["form"] == form_name
                and row["person"] == person_name
            ):
                print(
                    f"{row['verb_id']:7} | {row['verb']:10} | {row['form']:19} | {row['person']:12} | "
                    f"{row['conjugation_id']:14} | {row['hypothetical_regular_conjugation']}"
                )
                break


if __name__ == "__main__":
    generate_conjugation_table()
