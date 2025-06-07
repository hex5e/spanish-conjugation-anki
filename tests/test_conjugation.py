import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from generate_cards_init import conjugate_regular

@pytest.mark.parametrize("verb,form_id,person_id,expected", [
    ("hablar", 3, 11, "hablo"),                 # indicativo_presente, 1st singular
    ("comer", 4, 31, "comió"),                 # indicativo_preterito, 3rd singular
    ("vivir", 7, 22, "viviríais"),            # condicional, 2nd plural
    ("levantarse", 1, 0, "levantandose"),       # gerundio, reflexive
    ("ducharse", 6, 32, "se ducharán"),         # futuro, reflexive
    ("levantarse", 11, 21, "levantate"),        # imperativo afirmativo, reflexive
    ("levantarse", 12, 21, "no te levantes"),   # imperativo negativo, reflexive
])
def test_conjugate_regular(verb, form_id, person_id, expected):
    assert conjugate_regular(verb, form_id, person_id) == expected
