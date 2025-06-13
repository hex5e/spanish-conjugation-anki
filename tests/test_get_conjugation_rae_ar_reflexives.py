import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from get_conjugation_rae import RAEConjugationFetcher
from get_conjugation_rae import RAEConjugationTransformer


def test_darse():
    fetcher = RAEConjugationFetcher()
    raw = fetcher.get_conjugation("dar")
    transformer = RAEConjugationTransformer("darse", is_reflexive=True)
    out = transformer.transform(raw)

    assert out["infinitivo"] == "darse"
    assert out["gerundio"] == "dándose"
    assert out["participio"] == ""

    # Indicativo presente
    assert out["indicativo_presente"]["1st_singular"] == "me doy"
    assert out["indicativo_presente"]["2nd_singular"] == "te das"
    assert out["indicativo_presente"]["3rd_singular"] == "se da"
    assert out["indicativo_presente"]["1st_plural"] == "nos damos"
    assert out["indicativo_presente"]["2nd_plural"] == "os dais"
    assert out["indicativo_presente"]["3rd_plural"] == "se dan"

    # Indicativo pretérito
    assert out["indicativo_preterito"]["1st_singular"] == "me di"
    assert out["indicativo_preterito"]["2nd_singular"] == "te diste"
    assert out["indicativo_preterito"]["3rd_singular"] == "se dio"
    assert out["indicativo_preterito"]["1st_plural"] == "nos dimos"
    assert out["indicativo_preterito"]["2nd_plural"] == "os disteis"
    assert out["indicativo_preterito"]["3rd_plural"] == "se dieron"

    # Indicativo imperfecto
    assert out["indicativo_imperfecto"]["1st_singular"] == "me daba"
    assert out["indicativo_imperfecto"]["2nd_singular"] == "te dabas"
    assert out["indicativo_imperfecto"]["3rd_singular"] == "se daba"
    assert out["indicativo_imperfecto"]["1st_plural"] == "nos dábamos"
    assert out["indicativo_imperfecto"]["2nd_plural"] == "os dabais"
    assert out["indicativo_imperfecto"]["3rd_plural"] == "se daban"

    # Indicativo futuro
    assert out["indicativo_futuro"]["1st_singular"] == "me daré"
    assert out["indicativo_futuro"]["2nd_singular"] == "te darás"
    assert out["indicativo_futuro"]["3rd_singular"] == "se dará"
    assert out["indicativo_futuro"]["1st_plural"] == "nos daremos"
    assert out["indicativo_futuro"]["2nd_plural"] == "os daréis"
    assert out["indicativo_futuro"]["3rd_plural"] == "se darán"

    # Condicional
    assert out["condicional"]["1st_singular"] == "me daría"
    assert out["condicional"]["2nd_singular"] == "te darías"
    assert out["condicional"]["3rd_singular"] == "se daría"
    assert out["condicional"]["1st_plural"] == "nos daríamos"
    assert out["condicional"]["2nd_plural"] == "os daríais"
    assert out["condicional"]["3rd_plural"] == "se darían"

    # Subjuntivo presente
    assert out["subjuntivo_presente"]["1st_singular"] == "me dé"
    assert out["subjuntivo_presente"]["2nd_singular"] == "te des"
    assert out["subjuntivo_presente"]["3rd_singular"] == "se dé"
    assert out["subjuntivo_presente"]["1st_plural"] == "nos demos"
    assert out["subjuntivo_presente"]["2nd_plural"] == "os deis"
    assert out["subjuntivo_presente"]["3rd_plural"] == "se den"

    # Subjuntivo imperfecto
    assert out["subjuntivo_imperfecto"]["1st_singular"] == "me diera"
    assert out["subjuntivo_imperfecto"]["2nd_singular"] == "te dieras"
    assert out["subjuntivo_imperfecto"]["3rd_singular"] == "se diera"
    assert out["subjuntivo_imperfecto"]["1st_plural"] == "nos diéramos"
    assert out["subjuntivo_imperfecto"]["2nd_plural"] == "os dierais"
    assert out["subjuntivo_imperfecto"]["3rd_plural"] == "se dieran"

    # Subjuntivo futuro
    assert out["subjuntivo_futuro"]["1st_singular"] == "me diere"
    assert out["subjuntivo_futuro"]["2nd_singular"] == "te dieres"
    assert out["subjuntivo_futuro"]["3rd_singular"] == "se diere"
    assert out["subjuntivo_futuro"]["1st_plural"] == "nos diéremos"
    assert out["subjuntivo_futuro"]["2nd_plural"] == "os diereis"
    assert out["subjuntivo_futuro"]["3rd_plural"] == "se dieren"

    # Imperativo afirmativo
    assert out["imperativo_affirmativo"]["2nd_singular"] == "date"
    assert out["imperativo_affirmativo"]["3rd_singular"] == "dése"
    assert out["imperativo_affirmativo"]["1st_plural"] == "démonos"
    assert out["imperativo_affirmativo"]["2nd_plural"] == "daos"
    assert out["imperativo_affirmativo"]["3rd_plural"] == "dense"

    # Imperativo negativo
    assert out["imperativo_negativo"]["2nd_singular"] == "no te des"
    assert out["imperativo_negativo"]["3rd_singular"] == "no se dé"
    assert out["imperativo_negativo"]["1st_plural"] == "no nos demos"
    assert out["imperativo_negativo"]["2nd_plural"] == "no os deis"
    assert out["imperativo_negativo"]["3rd_plural"] == "no se den"


def test_liarse():
    fetcher = RAEConjugationFetcher()
    raw = fetcher.get_conjugation("liar")
    transformer = RAEConjugationTransformer("liarse", is_reflexive=True)
    out = transformer.transform(raw)

    assert out["infinitivo"] == "liarse"
    assert out["gerundio"] == "liándose"
    assert out["participio"] == ""

    # Indicativo presente
    assert out["indicativo_presente"]["1st_singular"] == "me lío"
    assert out["indicativo_presente"]["2nd_singular"] == "te lías"
    assert out["indicativo_presente"]["3rd_singular"] == "se lía"
    assert out["indicativo_presente"]["1st_plural"] == "nos liamos"
    assert out["indicativo_presente"]["2nd_plural"] == "os liáis"
    assert out["indicativo_presente"]["3rd_plural"] == "se lían"

    # Indicativo pretérito
    assert out["indicativo_preterito"]["1st_singular"] == "me lié"
    assert out["indicativo_preterito"]["2nd_singular"] == "te liaste"
    assert out["indicativo_preterito"]["3rd_singular"] == "se lió"
    assert out["indicativo_preterito"]["1st_plural"] == "nos liamos"
    assert out["indicativo_preterito"]["2nd_plural"] == "os liasteis"
    assert out["indicativo_preterito"]["3rd_plural"] == "se liaron"

    # Indicativo imperfecto
    assert out["indicativo_imperfecto"]["1st_singular"] == "me liaba"
    assert out["indicativo_imperfecto"]["2nd_singular"] == "te liabas"
    assert out["indicativo_imperfecto"]["3rd_singular"] == "se liaba"
    assert out["indicativo_imperfecto"]["1st_plural"] == "nos liábamos"
    assert out["indicativo_imperfecto"]["2nd_plural"] == "os liabais"
    assert out["indicativo_imperfecto"]["3rd_plural"] == "se liaban"

    # Indicativo futuro
    assert out["indicativo_futuro"]["1st_singular"] == "me liaré"
    assert out["indicativo_futuro"]["2nd_singular"] == "te liarás"
    assert out["indicativo_futuro"]["3rd_singular"] == "se liará"
    assert out["indicativo_futuro"]["1st_plural"] == "nos liaremos"
    assert out["indicativo_futuro"]["2nd_plural"] == "os liaréis"
    assert out["indicativo_futuro"]["3rd_plural"] == "se liarán"

    # Condicional
    assert out["condicional"]["1st_singular"] == "me liaría"
    assert out["condicional"]["2nd_singular"] == "te liarías"
    assert out["condicional"]["3rd_singular"] == "se liaría"
    assert out["condicional"]["1st_plural"] == "nos liaríamos"
    assert out["condicional"]["2nd_plural"] == "os liaríais"
    assert out["condicional"]["3rd_plural"] == "se liarían"

    # Subjuntivo presente
    assert out["subjuntivo_presente"]["1st_singular"] == "me líe"
    assert out["subjuntivo_presente"]["2nd_singular"] == "te líes"
    assert out["subjuntivo_presente"]["3rd_singular"] == "se líe"
    assert out["subjuntivo_presente"]["1st_plural"] == "nos liemos"
    assert out["subjuntivo_presente"]["2nd_plural"] == "os liéis"
    assert out["subjuntivo_presente"]["3rd_plural"] == "se líen"

    # Subjuntivo imperfecto
    assert out["subjuntivo_imperfecto"]["1st_singular"] == "me liara"
    assert out["subjuntivo_imperfecto"]["2nd_singular"] == "te liaras"
    assert out["subjuntivo_imperfecto"]["3rd_singular"] == "se liara"
    assert out["subjuntivo_imperfecto"]["1st_plural"] == "nos liáramos"
    assert out["subjuntivo_imperfecto"]["2nd_plural"] == "os liarais"
    assert out["subjuntivo_imperfecto"]["3rd_plural"] == "se liaran"

    # Subjuntivo futuro
    assert out["subjuntivo_futuro"]["1st_singular"] == "me liare"
    assert out["subjuntivo_futuro"]["2nd_singular"] == "te liares"
    assert out["subjuntivo_futuro"]["3rd_singular"] == "se liare"
    assert out["subjuntivo_futuro"]["1st_plural"] == "nos liáremos"
    assert out["subjuntivo_futuro"]["2nd_plural"] == "os liareis"
    assert out["subjuntivo_futuro"]["3rd_plural"] == "se liaren"

    # Imperativo afirmativo
    assert out["imperativo_affirmativo"]["2nd_singular"] == "líate"
    assert out["imperativo_affirmativo"]["3rd_singular"] == "líese"
    assert out["imperativo_affirmativo"]["1st_plural"] == "liémonos"
    assert out["imperativo_affirmativo"]["2nd_plural"] == "liaos"
    assert out["imperativo_affirmativo"]["3rd_plural"] == "líense"

    # Imperativo negativo
    assert out["imperativo_negativo"]["2nd_singular"] == "no te líes"
    assert out["imperativo_negativo"]["3rd_singular"] == "no se líe"
    assert out["imperativo_negativo"]["1st_plural"] == "no nos liemos"
    assert out["imperativo_negativo"]["2nd_plural"] == "no os liéis"
    assert out["imperativo_negativo"]["3rd_plural"] == "no se líen"


def test_bañarse():
    fetcher = RAEConjugationFetcher()
    raw = fetcher.get_conjugation("bañar")
    transformer = RAEConjugationTransformer("bañarse", is_reflexive=True)
    out = transformer.transform(raw)

    assert out["infinitivo"] == "bañarse"
    assert out["gerundio"] == "bañándose"
    assert out["participio"] == ""

    # Indicativo presente
    assert out["indicativo_presente"]["1st_singular"] == "me baño"
    assert out["indicativo_presente"]["2nd_singular"] == "te bañas"
    assert out["indicativo_presente"]["3rd_singular"] == "se baña"
    assert out["indicativo_presente"]["1st_plural"] == "nos bañamos"
    assert out["indicativo_presente"]["2nd_plural"] == "os bañáis"
    assert out["indicativo_presente"]["3rd_plural"] == "se bañan"

    # Indicativo pretérito
    assert out["indicativo_preterito"]["1st_singular"] == "me bañé"
    assert out["indicativo_preterito"]["2nd_singular"] == "te bañaste"
    assert out["indicativo_preterito"]["3rd_singular"] == "se bañó"
    assert out["indicativo_preterito"]["1st_plural"] == "nos bañamos"
    assert out["indicativo_preterito"]["2nd_plural"] == "os bañasteis"
    assert out["indicativo_preterito"]["3rd_plural"] == "se bañaron"

    # Indicativo imperfecto
    assert out["indicativo_imperfecto"]["1st_singular"] == "me bañaba"
    assert out["indicativo_imperfecto"]["2nd_singular"] == "te bañabas"
    assert out["indicativo_imperfecto"]["3rd_singular"] == "se bañaba"
    assert out["indicativo_imperfecto"]["1st_plural"] == "nos bañábamos"
    assert out["indicativo_imperfecto"]["2nd_plural"] == "os bañabais"
    assert out["indicativo_imperfecto"]["3rd_plural"] == "se bañaban"

    # Indicativo futuro
    assert out["indicativo_futuro"]["1st_singular"] == "me bañaré"
    assert out["indicativo_futuro"]["2nd_singular"] == "te bañarás"
    assert out["indicativo_futuro"]["3rd_singular"] == "se bañará"
    assert out["indicativo_futuro"]["1st_plural"] == "nos bañaremos"
    assert out["indicativo_futuro"]["2nd_plural"] == "os bañaréis"
    assert out["indicativo_futuro"]["3rd_plural"] == "se bañarán"

    # Condicional
    assert out["condicional"]["1st_singular"] == "me bañaría"
    assert out["condicional"]["2nd_singular"] == "te bañarías"
    assert out["condicional"]["3rd_singular"] == "se bañaría"
    assert out["condicional"]["1st_plural"] == "nos bañaríamos"
    assert out["condicional"]["2nd_plural"] == "os bañaríais"
    assert out["condicional"]["3rd_plural"] == "se bañarían"

    # Subjuntivo presente
    assert out["subjuntivo_presente"]["1st_singular"] == "me bañe"
    assert out["subjuntivo_presente"]["2nd_singular"] == "te bañes"
    assert out["subjuntivo_presente"]["3rd_singular"] == "se bañe"
    assert out["subjuntivo_presente"]["1st_plural"] == "nos bañemos"
    assert out["subjuntivo_presente"]["2nd_plural"] == "os bañéis"
    assert out["subjuntivo_presente"]["3rd_plural"] == "se bañen"

    # Subjuntivo imperfecto
    assert out["subjuntivo_imperfecto"]["1st_singular"] == "me bañara"
    assert out["subjuntivo_imperfecto"]["2nd_singular"] == "te bañaras"
    assert out["subjuntivo_imperfecto"]["3rd_singular"] == "se bañara"
    assert out["subjuntivo_imperfecto"]["1st_plural"] == "nos bañáramos"
    assert out["subjuntivo_imperfecto"]["2nd_plural"] == "os bañarais"
    assert out["subjuntivo_imperfecto"]["3rd_plural"] == "se bañaran"

    # Subjuntivo futuro
    assert out["subjuntivo_futuro"]["1st_singular"] == "me bañare"
    assert out["subjuntivo_futuro"]["2nd_singular"] == "te bañares"
    assert out["subjuntivo_futuro"]["3rd_singular"] == "se bañare"
    assert out["subjuntivo_futuro"]["1st_plural"] == "nos bañáremos"
    assert out["subjuntivo_futuro"]["2nd_plural"] == "os bañareis"
    assert out["subjuntivo_futuro"]["3rd_plural"] == "se bañaren"

    # Imperativo afirmativo
    assert out["imperativo_affirmativo"]["2nd_singular"] == "báñate"
    assert out["imperativo_affirmativo"]["3rd_singular"] == "báñese"
    assert out["imperativo_affirmativo"]["1st_plural"] == "bañémonos"
    assert out["imperativo_affirmativo"]["2nd_plural"] == "bañaos"
    assert out["imperativo_affirmativo"]["3rd_plural"] == "báñense"

    # Imperativo negativo
    assert out["imperativo_negativo"]["2nd_singular"] == "no te bañes"
    assert out["imperativo_negativo"]["3rd_singular"] == "no se bañe"
    assert out["imperativo_negativo"]["1st_plural"] == "no nos bañemos"
    assert out["imperativo_negativo"]["2nd_plural"] == "no os bañéis"
    assert out["imperativo_negativo"]["3rd_plural"] == "no se bañen"
