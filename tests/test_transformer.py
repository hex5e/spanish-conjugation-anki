import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
from get_conjugation_rae import RAEConjugationTransformer

RAW = {
    "Formas no personales": {
        "Infinitivo": {"": "meter"},
        "Gerundio": {"": "metiendo"},
        "Participio": {"": "metido"},
    },
    "Indicativo": {
        "Presente": {
            "yo": "meto",
            "tú": "metes",
            "usted": "mete",
            "él, ella": "mete",
            "nosotros, nosotras": "metemos",
            "vosotros, vosotras": "metéis",
            "ustedes": "meten",
            "ellos, ellas": "meten",
        }
    },
    "Subjuntivo": {
        "Presente": {
            "yo": "meta",
            "tú": "metas",
            "usted": "meta",
            "él, ella": "meta",
            "nosotros, nosotras": "metamos",
            "vosotros, vosotras": "metáis",
            "ustedes": "metan",
            "ellos, ellas": "metan",
        }
    },
    "Imperativo": {
        "Imperativo": {
            "tú": "mete",
            "usted": "meta",
            "vosotros, vosotras": "meted",
            "ustedes": "metan",
        }
    },
}


def test_reflexive_transform():
    transformer = RAEConjugationTransformer("meterse", is_reflexive=True)
    out = transformer.transform(RAW)
    assert out["infinitivo"] == "meterse"
    assert out["gerundio"] == "metiéndose"
    assert out["participio"] == ""
    assert out["indicativo_presente"]["1st_singular"] == "me meto"
    assert out["imperativo_affirmativo"]["2nd_singular"] == "metete"
    assert out["imperativo_negativo"]["2nd_singular"] == "no te metas"
