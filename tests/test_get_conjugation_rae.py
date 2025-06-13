import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
from get_conjugation_rae import RAEConjugationFetcher
from get_conjugation_rae import RAEConjugationTransformer


def test_amar():
    fetcher = RAEConjugationFetcher()
    raw = fetcher.get_conjugation("amar")
    transformer = RAEConjugationTransformer("amar")
    out = transformer.transform(raw)

    assert out["infinitivo"] == "amar"
    assert out["gerundio"] == "amando"
    assert out["participio"] == "amado"

    # Indicativo presente
    assert out["indicativo_presente"]["1st_singular"] == "amo"
    assert out["indicativo_presente"]["2nd_singular"] == "amas"
    assert out["indicativo_presente"]["3rd_singular"] == "ama"
    assert out["indicativo_presente"]["1st_plural"] == "amamos"
    assert out["indicativo_presente"]["2nd_plural"] == "amáis"
    assert out["indicativo_presente"]["3rd_plural"] == "aman"

    # Indicativo pretérito
    assert out["indicativo_preterito"]["1st_singular"] == "amé"
    assert out["indicativo_preterito"]["2nd_singular"] == "amaste"
    assert out["indicativo_preterito"]["3rd_singular"] == "amó"
    assert out["indicativo_preterito"]["1st_plural"] == "amamos"
    assert out["indicativo_preterito"]["2nd_plural"] == "amasteis"
    assert out["indicativo_preterito"]["3rd_plural"] == "amaron"

    # Indicativo imperfecto
    assert out["indicativo_imperfecto"]["1st_singular"] == "amaba"
    assert out["indicativo_imperfecto"]["2nd_singular"] == "amabas"
    assert out["indicativo_imperfecto"]["3rd_singular"] == "amaba"
    assert out["indicativo_imperfecto"]["1st_plural"] == "amábamos"
    assert out["indicativo_imperfecto"]["2nd_plural"] == "amabais"
    assert out["indicativo_imperfecto"]["3rd_plural"] == "amaban"

    # Indicativo futuro
    assert out["indicativo_futuro"]["1st_singular"] == "amaré"
    assert out["indicativo_futuro"]["2nd_singular"] == "amarás"
    assert out["indicativo_futuro"]["3rd_singular"] == "amará"
    assert out["indicativo_futuro"]["1st_plural"] == "amaremos"
    assert out["indicativo_futuro"]["2nd_plural"] == "amaréis"
    assert out["indicativo_futuro"]["3rd_plural"] == "amarán"

    # Condicional
    assert out["condicional"]["1st_singular"] == "amaría"
    assert out["condicional"]["2nd_singular"] == "amarías"
    assert out["condicional"]["3rd_singular"] == "amaría"
    assert out["condicional"]["1st_plural"] == "amaríamos"
    assert out["condicional"]["2nd_plural"] == "amaríais"
    assert out["condicional"]["3rd_plural"] == "amarían"

    # Subjuntivo presente
    assert out["subjuntivo_presente"]["1st_singular"] == "ame"
    assert out["subjuntivo_presente"]["2nd_singular"] == "ames"
    assert out["subjuntivo_presente"]["3rd_singular"] == "ame"
    assert out["subjuntivo_presente"]["1st_plural"] == "amemos"
    assert out["subjuntivo_presente"]["2nd_plural"] == "améis"
    assert out["subjuntivo_presente"]["3rd_plural"] == "amen"

    # Subjuntivo imperfecto
    assert out["subjuntivo_imperfecto"]["1st_singular"] == "amara"
    assert out["subjuntivo_imperfecto"]["2nd_singular"] == "amaras"
    assert out["subjuntivo_imperfecto"]["3rd_singular"] == "amara"
    assert out["subjuntivo_imperfecto"]["1st_plural"] == "amáramos"
    assert out["subjuntivo_imperfecto"]["2nd_plural"] == "amarais"
    assert out["subjuntivo_imperfecto"]["3rd_plural"] == "amaran"

    # Subjuntivo futuro
    assert out["subjuntivo_futuro"]["1st_singular"] == "amare"
    assert out["subjuntivo_futuro"]["2nd_singular"] == "amares"
    assert out["subjuntivo_futuro"]["3rd_singular"] == "amare"
    assert out["subjuntivo_futuro"]["1st_plural"] == "amáremos"
    assert out["subjuntivo_futuro"]["2nd_plural"] == "amareis"
    assert out["subjuntivo_futuro"]["3rd_plural"] == "amaren"

    # Imperativo afirmativo
    assert out["imperativo_affirmativo"]["2nd_singular"] == "ama"
    assert out["imperativo_affirmativo"]["3rd_singular"] == "ame"
    assert out["imperativo_affirmativo"]["1st_plural"] == "amemos"
    assert out["imperativo_affirmativo"]["2nd_plural"] == "amad"
    assert out["imperativo_affirmativo"]["3rd_plural"] == "amen"

    # Imperativo negativo
    assert out["imperativo_negativo"]["2nd_singular"] == "no ames"
    assert out["imperativo_negativo"]["3rd_singular"] == "no ame"
    assert out["imperativo_negativo"]["1st_plural"] == "no amemos"
    assert out["imperativo_negativo"]["2nd_plural"] == "no améis"
    assert out["imperativo_negativo"]["3rd_plural"] == "no amen"
