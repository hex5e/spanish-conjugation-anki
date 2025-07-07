import sqlite3
from pathlib import Path

import genanki

DECK_ID = 2059400110
MODEL_ID = 1593012861
DECK_NAME = "Spanish Conjugation"

FRONT_TEMPLATE = Path("anki_template/card_template_front.html").read_text(
    encoding="utf-8"
)
BACK_TEMPLATE = Path("anki_template/card_template_back.html").read_text(
    encoding="utf-8"
)

model = genanki.Model(
    MODEL_ID,
    "Spanish Conjugation Cloze",
    fields=[{"name": "Text"}, {"name": "Audio"}],
    templates=[{"name": "Card 1", "qfmt": FRONT_TEMPLATE, "afmt": BACK_TEMPLATE}],
    model_type=genanki.Model.CLOZE,
)

deck = genanki.Deck(DECK_ID, DECK_NAME)

conn = sqlite3.connect("cards.db")
conn.row_factory = sqlite3.Row
rows = [dict(row) for row in conn.execute("SELECT * FROM cards").fetchall()]

media_files = []

for row in rows:
    if any(v is None or (isinstance(v, str) and not v.strip()) for v in row.values()):
        continue

    sentence = row["example_sentence"]
    conjugation = row["conjugation"]
    cloze_sentence = sentence.replace(conjugation, f"{{{{c1::{conjugation}}}}}", 1)

    audio_path = Path(row["audio_path"])
    audio_tag = f"[sound:{audio_path.name}]"

    note = genanki.Note(
        model=model,
        fields=[cloze_sentence, audio_tag],
        guid=genanki.guid_for(row["conjugation_id"]),
    )
    deck.add_note(note)
    media_files.append(str(audio_path))

package = genanki.Package(deck, media_files)
package.write_to_file("spanish_conjugations.apkg")
