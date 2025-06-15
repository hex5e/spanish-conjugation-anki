import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
from utilities.get_conjugation_rae import RAEConjugationFetcher
from utilities.get_conjugation_rae import RAEConjugationTransformer


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
    assert out["imperativo_afirmativo"]["2nd_singular"] == "ama"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "ame"
    assert out["imperativo_afirmativo"]["1st_plural"] == "amemos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "amad"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "amen"

    # Imperativo negativo
    assert out["imperativo_negativo"]["2nd_singular"] == "no ames"
    assert out["imperativo_negativo"]["3rd_singular"] == "no ame"
    assert out["imperativo_negativo"]["1st_plural"] == "no amemos"
    assert out["imperativo_negativo"]["2nd_plural"] == "no améis"
    assert out["imperativo_negativo"]["3rd_plural"] == "no amen"


def test_ser():
    fetcher = RAEConjugationFetcher()
    raw = fetcher.get_conjugation("ser")
    transformer = RAEConjugationTransformer("ser")
    out = transformer.transform(raw)

    assert out["infinitivo"] == "ser"
    assert out["gerundio"] == "siendo"
    assert out["participio"] == "sido"

    # Indicativo presente
    assert out["indicativo_presente"]["1st_singular"] == "soy"
    assert out["indicativo_presente"]["2nd_singular"] == "eres"
    assert out["indicativo_presente"]["3rd_singular"] == "es"
    assert out["indicativo_presente"]["1st_plural"] == "somos"
    assert out["indicativo_presente"]["2nd_plural"] == "sois"
    assert out["indicativo_presente"]["3rd_plural"] == "son"

    # Indicativo pretérito
    assert out["indicativo_preterito"]["1st_singular"] == "fui"
    assert out["indicativo_preterito"]["2nd_singular"] == "fuiste"
    assert out["indicativo_preterito"]["3rd_singular"] == "fue"
    assert out["indicativo_preterito"]["1st_plural"] == "fuimos"
    assert out["indicativo_preterito"]["2nd_plural"] == "fuisteis"
    assert out["indicativo_preterito"]["3rd_plural"] == "fueron"

    # Indicativo imperfecto
    assert out["indicativo_imperfecto"]["1st_singular"] == "era"
    assert out["indicativo_imperfecto"]["2nd_singular"] == "eras"
    assert out["indicativo_imperfecto"]["3rd_singular"] == "era"
    assert out["indicativo_imperfecto"]["1st_plural"] == "éramos"
    assert out["indicativo_imperfecto"]["2nd_plural"] == "erais"
    assert out["indicativo_imperfecto"]["3rd_plural"] == "eran"

    # Indicativo futuro
    assert out["indicativo_futuro"]["1st_singular"] == "seré"
    assert out["indicativo_futuro"]["2nd_singular"] == "serás"
    assert out["indicativo_futuro"]["3rd_singular"] == "será"
    assert out["indicativo_futuro"]["1st_plural"] == "seremos"
    assert out["indicativo_futuro"]["2nd_plural"] == "seréis"
    assert out["indicativo_futuro"]["3rd_plural"] == "serán"

    # Condicional
    assert out["condicional"]["1st_singular"] == "sería"
    assert out["condicional"]["2nd_singular"] == "serías"
    assert out["condicional"]["3rd_singular"] == "sería"
    assert out["condicional"]["1st_plural"] == "seríamos"
    assert out["condicional"]["2nd_plural"] == "seríais"
    assert out["condicional"]["3rd_plural"] == "serían"

    # Subjuntivo presente
    assert out["subjuntivo_presente"]["1st_singular"] == "sea"
    assert out["subjuntivo_presente"]["2nd_singular"] == "seas"
    assert out["subjuntivo_presente"]["3rd_singular"] == "sea"
    assert out["subjuntivo_presente"]["1st_plural"] == "seamos"
    assert out["subjuntivo_presente"]["2nd_plural"] == "seáis"
    assert out["subjuntivo_presente"]["3rd_plural"] == "sean"

    # Subjuntivo imperfecto
    assert out["subjuntivo_imperfecto"]["1st_singular"] == "fuera"
    assert out["subjuntivo_imperfecto"]["2nd_singular"] == "fueras"
    assert out["subjuntivo_imperfecto"]["3rd_singular"] == "fuera"
    assert out["subjuntivo_imperfecto"]["1st_plural"] == "fuéramos"
    assert out["subjuntivo_imperfecto"]["2nd_plural"] == "fuerais"
    assert out["subjuntivo_imperfecto"]["3rd_plural"] == "fueran"

    # Subjuntivo futuro
    assert out["subjuntivo_futuro"]["1st_singular"] == "fuere"
    assert out["subjuntivo_futuro"]["2nd_singular"] == "fueres"
    assert out["subjuntivo_futuro"]["3rd_singular"] == "fuere"
    assert out["subjuntivo_futuro"]["1st_plural"] == "fuéremos"
    assert out["subjuntivo_futuro"]["2nd_plural"] == "fuereis"
    assert out["subjuntivo_futuro"]["3rd_plural"] == "fueren"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "sé"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "sea"
    assert out["imperativo_afirmativo"]["1st_plural"] == "seamos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "sed"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "sean"

    # Imperativo negativo
    assert out["imperativo_negativo"]["2nd_singular"] == "no seas"
    assert out["imperativo_negativo"]["3rd_singular"] == "no sea"
    assert out["imperativo_negativo"]["1st_plural"] == "no seamos"
    assert out["imperativo_negativo"]["2nd_plural"] == "no seáis"
    assert out["imperativo_negativo"]["3rd_plural"] == "no sean"


def test_recibir():
    fetcher = RAEConjugationFetcher()
    raw = fetcher.get_conjugation("recibir")
    transformer = RAEConjugationTransformer("recibir")
    out = transformer.transform(raw)

    assert out["infinitivo"] == "recibir"
    assert out["gerundio"] == "recibiendo"
    assert out["participio"] == "recibido"

    # Indicativo presente
    assert out["indicativo_presente"]["1st_singular"] == "recibo"
    assert out["indicativo_presente"]["2nd_singular"] == "recibes"
    assert out["indicativo_presente"]["3rd_singular"] == "recibe"
    assert out["indicativo_presente"]["1st_plural"] == "recibimos"
    assert out["indicativo_presente"]["2nd_plural"] == "recibís"
    assert out["indicativo_presente"]["3rd_plural"] == "reciben"

    # Indicativo pretérito
    assert out["indicativo_preterito"]["1st_singular"] == "recibí"
    assert out["indicativo_preterito"]["2nd_singular"] == "recibiste"
    assert out["indicativo_preterito"]["3rd_singular"] == "recibió"
    assert out["indicativo_preterito"]["1st_plural"] == "recibimos"
    assert out["indicativo_preterito"]["2nd_plural"] == "recibisteis"
    assert out["indicativo_preterito"]["3rd_plural"] == "recibieron"

    # Indicativo imperfecto
    assert out["indicativo_imperfecto"]["1st_singular"] == "recibía"
    assert out["indicativo_imperfecto"]["2nd_singular"] == "recibías"
    assert out["indicativo_imperfecto"]["3rd_singular"] == "recibía"
    assert out["indicativo_imperfecto"]["1st_plural"] == "recibíamos"
    assert out["indicativo_imperfecto"]["2nd_plural"] == "recibíais"
    assert out["indicativo_imperfecto"]["3rd_plural"] == "recibían"

    # Indicativo futuro
    assert out["indicativo_futuro"]["1st_singular"] == "recibiré"
    assert out["indicativo_futuro"]["2nd_singular"] == "recibirás"
    assert out["indicativo_futuro"]["3rd_singular"] == "recibirá"
    assert out["indicativo_futuro"]["1st_plural"] == "recibiremos"
    assert out["indicativo_futuro"]["2nd_plural"] == "recibiréis"
    assert out["indicativo_futuro"]["3rd_plural"] == "recibirán"

    # Condicional
    assert out["condicional"]["1st_singular"] == "recibiría"
    assert out["condicional"]["2nd_singular"] == "recibirías"
    assert out["condicional"]["3rd_singular"] == "recibiría"
    assert out["condicional"]["1st_plural"] == "recibiríamos"
    assert out["condicional"]["2nd_plural"] == "recibiríais"
    assert out["condicional"]["3rd_plural"] == "recibirían"

    # Subjuntivo presente
    assert out["subjuntivo_presente"]["1st_singular"] == "reciba"
    assert out["subjuntivo_presente"]["2nd_singular"] == "recibas"
    assert out["subjuntivo_presente"]["3rd_singular"] == "reciba"
    assert out["subjuntivo_presente"]["1st_plural"] == "recibamos"
    assert out["subjuntivo_presente"]["2nd_plural"] == "recibáis"
    assert out["subjuntivo_presente"]["3rd_plural"] == "reciban"

    # Subjuntivo imperfecto
    assert out["subjuntivo_imperfecto"]["1st_singular"] == "recibiera"
    assert out["subjuntivo_imperfecto"]["2nd_singular"] == "recibieras"
    assert out["subjuntivo_imperfecto"]["3rd_singular"] == "recibiera"
    assert out["subjuntivo_imperfecto"]["1st_plural"] == "recibiéramos"
    assert out["subjuntivo_imperfecto"]["2nd_plural"] == "recibierais"
    assert out["subjuntivo_imperfecto"]["3rd_plural"] == "recibieran"

    # Subjuntivo futuro
    assert out["subjuntivo_futuro"]["1st_singular"] == "recibiere"
    assert out["subjuntivo_futuro"]["2nd_singular"] == "recibieres"
    assert out["subjuntivo_futuro"]["3rd_singular"] == "recibiere"
    assert out["subjuntivo_futuro"]["1st_plural"] == "recibiéremos"
    assert out["subjuntivo_futuro"]["2nd_plural"] == "recibiereis"
    assert out["subjuntivo_futuro"]["3rd_plural"] == "recibieren"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "recibe"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "reciba"
    assert out["imperativo_afirmativo"]["1st_plural"] == "recibamos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "recibid"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "reciban"

    # Imperativo negativo
    assert out["imperativo_negativo"]["2nd_singular"] == "no recibas"
    assert out["imperativo_negativo"]["3rd_singular"] == "no reciba"
    assert out["imperativo_negativo"]["1st_plural"] == "no recibamos"
    assert out["imperativo_negativo"]["2nd_plural"] == "no recibáis"
    assert out["imperativo_negativo"]["3rd_plural"] == "no reciban"


def test_oír():
    fetcher = RAEConjugationFetcher()
    raw = fetcher.get_conjugation("oír")
    transformer = RAEConjugationTransformer("oír")
    out = transformer.transform(raw)

    assert out["infinitivo"] == "oír"
    assert out["gerundio"] == "oyendo"
    assert out["participio"] == "oído"

    # Indicativo presente
    assert out["indicativo_presente"]["1st_singular"] == "oigo"
    assert out["indicativo_presente"]["2nd_singular"] == "oyes"
    assert out["indicativo_presente"]["3rd_singular"] == "oye"
    assert out["indicativo_presente"]["1st_plural"] == "oímos"
    assert out["indicativo_presente"]["2nd_plural"] == "oís"
    assert out["indicativo_presente"]["3rd_plural"] == "oyen"

    # Indicativo pretérito
    assert out["indicativo_preterito"]["1st_singular"] == "oí"
    assert out["indicativo_preterito"]["2nd_singular"] == "oíste"
    assert out["indicativo_preterito"]["3rd_singular"] == "oyó"
    assert out["indicativo_preterito"]["1st_plural"] == "oímos"
    assert out["indicativo_preterito"]["2nd_plural"] == "oísteis"
    assert out["indicativo_preterito"]["3rd_plural"] == "oyeron"

    # Indicativo imperfecto
    assert out["indicativo_imperfecto"]["1st_singular"] == "oía"
    assert out["indicativo_imperfecto"]["2nd_singular"] == "oías"
    assert out["indicativo_imperfecto"]["3rd_singular"] == "oía"
    assert out["indicativo_imperfecto"]["1st_plural"] == "oíamos"
    assert out["indicativo_imperfecto"]["2nd_plural"] == "oíais"
    assert out["indicativo_imperfecto"]["3rd_plural"] == "oían"

    # Indicativo futuro
    assert out["indicativo_futuro"]["1st_singular"] == "oiré"
    assert out["indicativo_futuro"]["2nd_singular"] == "oirás"
    assert out["indicativo_futuro"]["3rd_singular"] == "oirá"
    assert out["indicativo_futuro"]["1st_plural"] == "oiremos"
    assert out["indicativo_futuro"]["2nd_plural"] == "oiréis"
    assert out["indicativo_futuro"]["3rd_plural"] == "oirán"

    # Condicional
    assert out["condicional"]["1st_singular"] == "oiría"
    assert out["condicional"]["2nd_singular"] == "oirías"
    assert out["condicional"]["3rd_singular"] == "oiría"
    assert out["condicional"]["1st_plural"] == "oiríamos"
    assert out["condicional"]["2nd_plural"] == "oiríais"
    assert out["condicional"]["3rd_plural"] == "oirían"

    # Subjuntivo presente
    assert out["subjuntivo_presente"]["1st_singular"] == "oiga"
    assert out["subjuntivo_presente"]["2nd_singular"] == "oigas"
    assert out["subjuntivo_presente"]["3rd_singular"] == "oiga"
    assert out["subjuntivo_presente"]["1st_plural"] == "oigamos"
    assert out["subjuntivo_presente"]["2nd_plural"] == "oigáis"
    assert out["subjuntivo_presente"]["3rd_plural"] == "oigan"

    # Subjuntivo imperfecto
    assert out["subjuntivo_imperfecto"]["1st_singular"] == "oyera"
    assert out["subjuntivo_imperfecto"]["2nd_singular"] == "oyeras"
    assert out["subjuntivo_imperfecto"]["3rd_singular"] == "oyera"
    assert out["subjuntivo_imperfecto"]["1st_plural"] == "oyéramos"
    assert out["subjuntivo_imperfecto"]["2nd_plural"] == "oyerais"
    assert out["subjuntivo_imperfecto"]["3rd_plural"] == "oyeran"

    # Subjuntivo futuro
    assert out["subjuntivo_futuro"]["1st_singular"] == "oyere"
    assert out["subjuntivo_futuro"]["2nd_singular"] == "oyeres"
    assert out["subjuntivo_futuro"]["3rd_singular"] == "oyere"
    assert out["subjuntivo_futuro"]["1st_plural"] == "oyéremos"
    assert out["subjuntivo_futuro"]["2nd_plural"] == "oyereis"
    assert out["subjuntivo_futuro"]["3rd_plural"] == "oyeren"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "oye"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "oiga"
    assert out["imperativo_afirmativo"]["1st_plural"] == "oigamos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "oíd"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "oigan"

    # Imperativo negativo
    assert out["imperativo_negativo"]["2nd_singular"] == "no oigas"
    assert out["imperativo_negativo"]["3rd_singular"] == "no oiga"
    assert out["imperativo_negativo"]["1st_plural"] == "no oigamos"
    assert out["imperativo_negativo"]["2nd_plural"] == "no oigáis"
    assert out["imperativo_negativo"]["3rd_plural"] == "no oigan"
