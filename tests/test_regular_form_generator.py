import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from regular_form_generator import RegularFormGenerator

gen = RegularFormGenerator()


def test_hablar():
    # Non-personal forms
    assert gen.generate("hablar", "infinitivo", "not_applicable") == "hablar"
    assert gen.generate("hablar", "gerundio", "not_applicable") == "hablando"
    assert gen.generate("hablar", "participio", "not_applicable") == "hablado"

    # Indicativo presente
    assert gen.generate("hablar", "indicativo_presente", "1st_singular") == "hablo"
    assert gen.generate("hablar", "indicativo_presente", "2nd_singular") == "hablas"
    assert gen.generate("hablar", "indicativo_presente", "3rd_singular") == "habla"
    assert gen.generate("hablar", "indicativo_presente", "1st_plural") == "hablamos"
    assert gen.generate("hablar", "indicativo_presente", "2nd_plural") == "habláis"
    assert gen.generate("hablar", "indicativo_presente", "3rd_plural") == "hablan"

    # Indicativo pretérito
    assert gen.generate("hablar", "indicativo_preterito", "1st_singular") == "hablé"
    assert gen.generate("hablar", "indicativo_preterito", "2nd_singular") == "hablaste"
    assert gen.generate("hablar", "indicativo_preterito", "3rd_singular") == "habló"
    assert gen.generate("hablar", "indicativo_preterito", "1st_plural") == "hablamos"
    assert gen.generate("hablar", "indicativo_preterito", "2nd_plural") == "hablasteis"
    assert gen.generate("hablar", "indicativo_preterito", "3rd_plural") == "hablaron"

    # Indicativo imperfecto
    assert gen.generate("hablar", "indicativo_imperfecto", "1st_singular") == "hablaba"
    assert gen.generate("hablar", "indicativo_imperfecto", "2nd_singular") == "hablabas"
    assert gen.generate("hablar", "indicativo_imperfecto", "3rd_singular") == "hablaba"
    assert gen.generate("hablar", "indicativo_imperfecto", "1st_plural") == "hablábamos"
    assert gen.generate("hablar", "indicativo_imperfecto", "2nd_plural") == "hablabais"
    assert gen.generate("hablar", "indicativo_imperfecto", "3rd_plural") == "hablaban"

    # Indicativo futuro
    assert gen.generate("hablar", "indicativo_futuro", "1st_singular") == "hablaré"
    assert gen.generate("hablar", "indicativo_futuro", "2nd_singular") == "hablarás"
    assert gen.generate("hablar", "indicativo_futuro", "3rd_singular") == "hablará"
    assert gen.generate("hablar", "indicativo_futuro", "1st_plural") == "hablaremos"
    assert gen.generate("hablar", "indicativo_futuro", "2nd_plural") == "hablaréis"
    assert gen.generate("hablar", "indicativo_futuro", "3rd_plural") == "hablarán"

    # Condicional
    assert gen.generate("hablar", "condicional", "1st_singular") == "hablaría"
    assert gen.generate("hablar", "condicional", "2nd_singular") == "hablarías"
    assert gen.generate("hablar", "condicional", "3rd_singular") == "hablaría"
    assert gen.generate("hablar", "condicional", "1st_plural") == "hablaríamos"
    assert gen.generate("hablar", "condicional", "2nd_plural") == "hablaríais"
    assert gen.generate("hablar", "condicional", "3rd_plural") == "hablarían"

    # Subjuntivo presente
    assert gen.generate("hablar", "subjuntivo_presente", "1st_singular") == "hable"
    assert gen.generate("hablar", "subjuntivo_presente", "2nd_singular") == "hables"
    assert gen.generate("hablar", "subjuntivo_presente", "3rd_singular") == "hable"
    assert gen.generate("hablar", "subjuntivo_presente", "1st_plural") == "hablemos"
    assert gen.generate("hablar", "subjuntivo_presente", "2nd_plural") == "habléis"
    assert gen.generate("hablar", "subjuntivo_presente", "3rd_plural") == "hablen"

    # Subjuntivo imperfecto
    assert gen.generate("hablar", "subjuntivo_imperfecto", "1st_singular") == "hablara"
    assert gen.generate("hablar", "subjuntivo_imperfecto", "2nd_singular") == "hablaras"
    assert gen.generate("hablar", "subjuntivo_imperfecto", "3rd_singular") == "hablara"
    assert gen.generate("hablar", "subjuntivo_imperfecto", "1st_plural") == "habláramos"
    assert gen.generate("hablar", "subjuntivo_imperfecto", "2nd_plural") == "hablarais"
    assert gen.generate("hablar", "subjuntivo_imperfecto", "3rd_plural") == "hablaran"

    # Subjuntivo futuro (rarely used in modern Spanish)
    assert gen.generate("hablar", "subjuntivo_futuro", "1st_singular") == "hablare"
    assert gen.generate("hablar", "subjuntivo_futuro", "2nd_singular") == "hablares"
    assert gen.generate("hablar", "subjuntivo_futuro", "3rd_singular") == "hablare"
    assert gen.generate("hablar", "subjuntivo_futuro", "1st_plural") == "habláremos"
    assert gen.generate("hablar", "subjuntivo_futuro", "2nd_plural") == "hablareis"
    assert gen.generate("hablar", "subjuntivo_futuro", "3rd_plural") == "hablaren"

    # Imperativo afirmativo (no 1st person singular)
    assert gen.generate("hablar", "imperativo_affirmativo", "2nd_singular") == "habla"
    assert gen.generate("hablar", "imperativo_affirmativo", "3rd_singular") == "hable"
    assert gen.generate("hablar", "imperativo_affirmativo", "1st_plural") == "hablemos"
    assert gen.generate("hablar", "imperativo_affirmativo", "2nd_plural") == "hablad"
    assert gen.generate("hablar", "imperativo_affirmativo", "3rd_plural") == "hablen"

    # Imperativo negativo (no 1st person singular)
    assert gen.generate("hablar", "imperativo_negativo", "2nd_singular") == "no hables"
    assert gen.generate("hablar", "imperativo_negativo", "3rd_singular") == "no hable"
    assert gen.generate("hablar", "imperativo_negativo", "1st_plural") == "no hablemos"
    assert gen.generate("hablar", "imperativo_negativo", "2nd_plural") == "no habléis"
    assert gen.generate("hablar", "imperativo_negativo", "3rd_plural") == "no hablen"


def test_deber():
    # Non-personal forms
    assert gen.generate("deber", "infinitivo", "not_applicable") == "deber"
    assert gen.generate("deber", "gerundio", "not_applicable") == "debiendo"
    assert gen.generate("deber", "participio", "not_applicable") == "debido"

    # Indicativo presente
    assert gen.generate("deber", "indicativo_presente", "1st_singular") == "debo"
    assert gen.generate("deber", "indicativo_presente", "2nd_singular") == "debes"
    assert gen.generate("deber", "indicativo_presente", "3rd_singular") == "debe"
    assert gen.generate("deber", "indicativo_presente", "1st_plural") == "debemos"
    assert gen.generate("deber", "indicativo_presente", "2nd_plural") == "debéis"
    assert gen.generate("deber", "indicativo_presente", "3rd_plural") == "deben"

    # Indicativo pretérito
    assert gen.generate("deber", "indicativo_preterito", "1st_singular") == "debí"
    assert gen.generate("deber", "indicativo_preterito", "2nd_singular") == "debiste"
    assert gen.generate("deber", "indicativo_preterito", "3rd_singular") == "debió"
    assert gen.generate("deber", "indicativo_preterito", "1st_plural") == "debimos"
    assert gen.generate("deber", "indicativo_preterito", "2nd_plural") == "debisteis"
    assert gen.generate("deber", "indicativo_preterito", "3rd_plural") == "debieron"

    # Indicativo imperfecto
    assert gen.generate("deber", "indicativo_imperfecto", "1st_singular") == "debía"
    assert gen.generate("deber", "indicativo_imperfecto", "2nd_singular") == "debías"
    assert gen.generate("deber", "indicativo_imperfecto", "3rd_singular") == "debía"
    assert gen.generate("deber", "indicativo_imperfecto", "1st_plural") == "debíamos"
    assert gen.generate("deber", "indicativo_imperfecto", "2nd_plural") == "debíais"
    assert gen.generate("deber", "indicativo_imperfecto", "3rd_plural") == "debían"

    # Indicativo futuro
    assert gen.generate("deber", "indicativo_futuro", "1st_singular") == "deberé"
    assert gen.generate("deber", "indicativo_futuro", "2nd_singular") == "deberás"
    assert gen.generate("deber", "indicativo_futuro", "3rd_singular") == "deberá"
    assert gen.generate("deber", "indicativo_futuro", "1st_plural") == "deberemos"
    assert gen.generate("deber", "indicativo_futuro", "2nd_plural") == "deberéis"
    assert gen.generate("deber", "indicativo_futuro", "3rd_plural") == "deberán"

    # Condicional
    assert gen.generate("deber", "condicional", "1st_singular") == "debería"
    assert gen.generate("deber", "condicional", "2nd_singular") == "deberías"
    assert gen.generate("deber", "condicional", "3rd_singular") == "debería"
    assert gen.generate("deber", "condicional", "1st_plural") == "deberíamos"
    assert gen.generate("deber", "condicional", "2nd_plural") == "deberíais"
    assert gen.generate("deber", "condicional", "3rd_plural") == "deberían"

    # Subjuntivo presente
    assert gen.generate("deber", "subjuntivo_presente", "1st_singular") == "deba"
    assert gen.generate("deber", "subjuntivo_presente", "2nd_singular") == "debas"
    assert gen.generate("deber", "subjuntivo_presente", "3rd_singular") == "deba"
    assert gen.generate("deber", "subjuntivo_presente", "1st_plural") == "debamos"
    assert gen.generate("deber", "subjuntivo_presente", "2nd_plural") == "debáis"
    assert gen.generate("deber", "subjuntivo_presente", "3rd_plural") == "deban"

    # Subjuntivo imperfecto (using -era forms)
    assert gen.generate("deber", "subjuntivo_imperfecto", "1st_singular") == "debiera"
    assert gen.generate("deber", "subjuntivo_imperfecto", "2nd_singular") == "debieras"
    assert gen.generate("deber", "subjuntivo_imperfecto", "3rd_singular") == "debiera"
    assert gen.generate("deber", "subjuntivo_imperfecto", "1st_plural") == "debiéramos"
    assert gen.generate("deber", "subjuntivo_imperfecto", "2nd_plural") == "debierais"
    assert gen.generate("deber", "subjuntivo_imperfecto", "3rd_plural") == "debieran"

    # Subjuntivo futuro (rarely used in modern Spanish)
    assert gen.generate("deber", "subjuntivo_futuro", "1st_singular") == "debiere"
    assert gen.generate("deber", "subjuntivo_futuro", "2nd_singular") == "debieres"
    assert gen.generate("deber", "subjuntivo_futuro", "3rd_singular") == "debiere"
    assert gen.generate("deber", "subjuntivo_futuro", "1st_plural") == "debiéremos"
    assert gen.generate("deber", "subjuntivo_futuro", "2nd_plural") == "debiereis"
    assert gen.generate("deber", "subjuntivo_futuro", "3rd_plural") == "debieren"

    # Imperativo afirmativo (no 1st person singular)
    assert gen.generate("deber", "imperativo_affirmativo", "2nd_singular") == "debe"
    assert gen.generate("deber", "imperativo_affirmativo", "3rd_singular") == "deba"
    assert gen.generate("deber", "imperativo_affirmativo", "1st_plural") == "debamos"
    assert gen.generate("deber", "imperativo_affirmativo", "2nd_plural") == "debed"
    assert gen.generate("deber", "imperativo_affirmativo", "3rd_plural") == "deban"

    # Imperativo negativo (no 1st person singular)
    assert gen.generate("deber", "imperativo_negativo", "2nd_singular") == "no debas"
    assert gen.generate("deber", "imperativo_negativo", "3rd_singular") == "no deba"
    assert gen.generate("deber", "imperativo_negativo", "1st_plural") == "no debamos"
    assert gen.generate("deber", "imperativo_negativo", "2nd_plural") == "no debáis"
    assert gen.generate("deber", "imperativo_negativo", "3rd_plural") == "no deban"


def test_vivir():
    # Non-personal forms
    assert gen.generate("vivir", "infinitivo", "not_applicable") == "vivir"
    assert gen.generate("vivir", "gerundio", "not_applicable") == "viviendo"
    assert gen.generate("vivir", "participio", "not_applicable") == "vivido"

    # Indicativo presente
    assert gen.generate("vivir", "indicativo_presente", "1st_singular") == "vivo"
    assert gen.generate("vivir", "indicativo_presente", "2nd_singular") == "vives"
    assert gen.generate("vivir", "indicativo_presente", "3rd_singular") == "vive"
    assert gen.generate("vivir", "indicativo_presente", "1st_plural") == "vivimos"
    assert gen.generate("vivir", "indicativo_presente", "2nd_plural") == "vivís"
    assert gen.generate("vivir", "indicativo_presente", "3rd_plural") == "viven"

    # Indicativo pretérito
    assert gen.generate("vivir", "indicativo_preterito", "1st_singular") == "viví"
    assert gen.generate("vivir", "indicativo_preterito", "2nd_singular") == "viviste"
    assert gen.generate("vivir", "indicativo_preterito", "3rd_singular") == "vivió"
    assert gen.generate("vivir", "indicativo_preterito", "1st_plural") == "vivimos"
    assert gen.generate("vivir", "indicativo_preterito", "2nd_plural") == "vivisteis"
    assert gen.generate("vivir", "indicativo_preterito", "3rd_plural") == "vivieron"

    # Indicativo imperfecto
    assert gen.generate("vivir", "indicativo_imperfecto", "1st_singular") == "vivía"
    assert gen.generate("vivir", "indicativo_imperfecto", "2nd_singular") == "vivías"
    assert gen.generate("vivir", "indicativo_imperfecto", "3rd_singular") == "vivía"
    assert gen.generate("vivir", "indicativo_imperfecto", "1st_plural") == "vivíamos"
    assert gen.generate("vivir", "indicativo_imperfecto", "2nd_plural") == "vivíais"
    assert gen.generate("vivir", "indicativo_imperfecto", "3rd_plural") == "vivían"

    # Indicativo futuro
    assert gen.generate("vivir", "indicativo_futuro", "1st_singular") == "viviré"
    assert gen.generate("vivir", "indicativo_futuro", "2nd_singular") == "vivirás"
    assert gen.generate("vivir", "indicativo_futuro", "3rd_singular") == "vivirá"
    assert gen.generate("vivir", "indicativo_futuro", "1st_plural") == "viviremos"
    assert gen.generate("vivir", "indicativo_futuro", "2nd_plural") == "viviréis"
    assert gen.generate("vivir", "indicativo_futuro", "3rd_plural") == "vivirán"

    # Condicional
    assert gen.generate("vivir", "condicional", "1st_singular") == "viviría"
    assert gen.generate("vivir", "condicional", "2nd_singular") == "vivirías"
    assert gen.generate("vivir", "condicional", "3rd_singular") == "viviría"
    assert gen.generate("vivir", "condicional", "1st_plural") == "viviríamos"
    assert gen.generate("vivir", "condicional", "2nd_plural") == "viviríais"
    assert gen.generate("vivir", "condicional", "3rd_plural") == "vivirían"

    # Subjuntivo presente
    assert gen.generate("vivir", "subjuntivo_presente", "1st_singular") == "viva"
    assert gen.generate("vivir", "subjuntivo_presente", "2nd_singular") == "vivas"
    assert gen.generate("vivir", "subjuntivo_presente", "3rd_singular") == "viva"
    assert gen.generate("vivir", "subjuntivo_presente", "1st_plural") == "vivamos"
    assert gen.generate("vivir", "subjuntivo_presente", "2nd_plural") == "viváis"
    assert gen.generate("vivir", "subjuntivo_presente", "3rd_plural") == "vivan"

    # Subjuntivo imperfecto (using -era forms)
    assert gen.generate("vivir", "subjuntivo_imperfecto", "1st_singular") == "viviera"
    assert gen.generate("vivir", "subjuntivo_imperfecto", "2nd_singular") == "vivieras"
    assert gen.generate("vivir", "subjuntivo_imperfecto", "3rd_singular") == "viviera"
    assert gen.generate("vivir", "subjuntivo_imperfecto", "1st_plural") == "viviéramos"
    assert gen.generate("vivir", "subjuntivo_imperfecto", "2nd_plural") == "vivierais"
    assert gen.generate("vivir", "subjuntivo_imperfecto", "3rd_plural") == "vivieran"

    # Subjuntivo futuro (rarely used in modern Spanish)
    assert gen.generate("vivir", "subjuntivo_futuro", "1st_singular") == "viviere"
    assert gen.generate("vivir", "subjuntivo_futuro", "2nd_singular") == "vivieres"
    assert gen.generate("vivir", "subjuntivo_futuro", "3rd_singular") == "viviere"
    assert gen.generate("vivir", "subjuntivo_futuro", "1st_plural") == "viviéremos"
    assert gen.generate("vivir", "subjuntivo_futuro", "2nd_plural") == "viviereis"
    assert gen.generate("vivir", "subjuntivo_futuro", "3rd_plural") == "vivieren"

    # Imperativo afirmativo (no 1st person singular)
    assert gen.generate("vivir", "imperativo_affirmativo", "2nd_singular") == "vive"
    assert gen.generate("vivir", "imperativo_affirmativo", "3rd_singular") == "viva"
    assert gen.generate("vivir", "imperativo_affirmativo", "1st_plural") == "vivamos"
    assert gen.generate("vivir", "imperativo_affirmativo", "2nd_plural") == "vivid"
    assert gen.generate("vivir", "imperativo_affirmativo", "3rd_plural") == "vivan"

    # Imperativo negativo (no 1st person singular)
    assert gen.generate("vivir", "imperativo_negativo", "2nd_singular") == "no vivas"
    assert gen.generate("vivir", "imperativo_negativo", "3rd_singular") == "no viva"
    assert gen.generate("vivir", "imperativo_negativo", "1st_plural") == "no vivamos"
    assert gen.generate("vivir", "imperativo_negativo", "2nd_plural") == "no viváis"
    assert gen.generate("vivir", "imperativo_negativo", "3rd_plural") == "no vivan"


def test_oír():
    # Non-personal forms
    assert gen.generate("oír", "infinitivo", "not_applicable") == "oír"
    assert gen.generate("oír", "gerundio", "not_applicable") == "oiendo"
    assert gen.generate("oír", "participio", "not_applicable") == "oido"

    # Indicativo presente
    assert gen.generate("oír", "indicativo_presente", "1st_singular") == "oo"
    assert gen.generate("oír", "indicativo_presente", "2nd_singular") == "oes"
    assert gen.generate("oír", "indicativo_presente", "3rd_singular") == "oe"
    assert gen.generate("oír", "indicativo_presente", "1st_plural") == "oimos"
    assert gen.generate("oír", "indicativo_presente", "2nd_plural") == "oís"
    assert gen.generate("oír", "indicativo_presente", "3rd_plural") == "oen"

    # Indicativo pretérito
    assert gen.generate("oír", "indicativo_preterito", "1st_singular") == "oí"
    assert gen.generate("oír", "indicativo_preterito", "2nd_singular") == "oiste"
    assert gen.generate("oír", "indicativo_preterito", "3rd_singular") == "oió"
    assert gen.generate("oír", "indicativo_preterito", "1st_plural") == "oimos"
    assert gen.generate("oír", "indicativo_preterito", "2nd_plural") == "oisteis"
    assert gen.generate("oír", "indicativo_preterito", "3rd_plural") == "oieron"

    # Indicativo imperfecto
    assert gen.generate("oír", "indicativo_imperfecto", "1st_singular") == "oía"
    assert gen.generate("oír", "indicativo_imperfecto", "2nd_singular") == "oías"
    assert gen.generate("oír", "indicativo_imperfecto", "3rd_singular") == "oía"
    assert gen.generate("oír", "indicativo_imperfecto", "1st_plural") == "oíamos"
    assert gen.generate("oír", "indicativo_imperfecto", "2nd_plural") == "oíais"
    assert gen.generate("oír", "indicativo_imperfecto", "3rd_plural") == "oían"

    # Indicativo futuro
    assert gen.generate("oír", "indicativo_futuro", "1st_singular") == "oíré"
    assert gen.generate("oír", "indicativo_futuro", "2nd_singular") == "oírás"
    assert gen.generate("oír", "indicativo_futuro", "3rd_singular") == "oírá"
    assert gen.generate("oír", "indicativo_futuro", "1st_plural") == "oíremos"
    assert gen.generate("oír", "indicativo_futuro", "2nd_plural") == "oíréis"
    assert gen.generate("oír", "indicativo_futuro", "3rd_plural") == "oírán"

    # Condicional
    assert gen.generate("oír", "condicional", "1st_singular") == "oíría"
    assert gen.generate("oír", "condicional", "2nd_singular") == "oírías"
    assert gen.generate("oír", "condicional", "3rd_singular") == "oíría"
    assert gen.generate("oír", "condicional", "1st_plural") == "oíríamos"
    assert gen.generate("oír", "condicional", "2nd_plural") == "oíríais"
    assert gen.generate("oír", "condicional", "3rd_plural") == "oírían"

    # Subjuntivo presente
    assert gen.generate("oír", "subjuntivo_presente", "1st_singular") == "oa"
    assert gen.generate("oír", "subjuntivo_presente", "2nd_singular") == "oas"
    assert gen.generate("oír", "subjuntivo_presente", "3rd_singular") == "oa"
    assert gen.generate("oír", "subjuntivo_presente", "1st_plural") == "oamos"
    assert gen.generate("oír", "subjuntivo_presente", "2nd_plural") == "oáis"
    assert gen.generate("oír", "subjuntivo_presente", "3rd_plural") == "oan"

    # Subjuntivo imperfecto
    assert gen.generate("oír", "subjuntivo_imperfecto", "1st_singular") == "oiera"
    assert gen.generate("oír", "subjuntivo_imperfecto", "2nd_singular") == "oieras"
    assert gen.generate("oír", "subjuntivo_imperfecto", "3rd_singular") == "oiera"
    assert gen.generate("oír", "subjuntivo_imperfecto", "1st_plural") == "oiéramos"
    assert gen.generate("oír", "subjuntivo_imperfecto", "2nd_plural") == "oierais"
    assert gen.generate("oír", "subjuntivo_imperfecto", "3rd_plural") == "oieran"

    # Subjuntivo futuro
    assert gen.generate("oír", "subjuntivo_futuro", "1st_singular") == "oiere"
    assert gen.generate("oír", "subjuntivo_futuro", "2nd_singular") == "oieres"
    assert gen.generate("oír", "subjuntivo_futuro", "3rd_singular") == "oiere"
    assert gen.generate("oír", "subjuntivo_futuro", "1st_plural") == "oiéremos"
    assert gen.generate("oír", "subjuntivo_futuro", "2nd_plural") == "oiereis"
    assert gen.generate("oír", "subjuntivo_futuro", "3rd_plural") == "oieren"

    # Imperativo afirmativo (no 1st person singular)
    assert gen.generate("oír", "imperativo_affirmativo", "2nd_singular") == "oe"
    assert gen.generate("oír", "imperativo_affirmativo", "3rd_singular") == "oa"
    assert gen.generate("oír", "imperativo_affirmativo", "1st_plural") == "oamos"
    assert gen.generate("oír", "imperativo_affirmativo", "2nd_plural") == "oid"
    assert gen.generate("oír", "imperativo_affirmativo", "3rd_plural") == "oan"

    # Imperativo negativo (no 1st person singular)
    assert gen.generate("oír", "imperativo_negativo", "2nd_singular") == "no oas"
    assert gen.generate("oír", "imperativo_negativo", "3rd_singular") == "no oa"
    assert gen.generate("oír", "imperativo_negativo", "1st_plural") == "no oamos"
    assert gen.generate("oír", "imperativo_negativo", "2nd_plural") == "no oáis"
    assert gen.generate("oír", "imperativo_negativo", "3rd_plural") == "no oan"


def test_levantarse():
    # Non-personal forms
    assert gen.generate("levantarse", "infinitivo", "not_applicable") == "levantarse"
    assert gen.generate("levantarse", "gerundio", "not_applicable") == "levantándose"
    assert gen.generate("levantarse", "participio", "not_applicable") == ""

    # Indicativo presente
    assert (
        gen.generate("levantarse", "indicativo_presente", "1st_singular")
        == "me levanto"
    )
    assert (
        gen.generate("levantarse", "indicativo_presente", "2nd_singular")
        == "te levantas"
    )
    assert (
        gen.generate("levantarse", "indicativo_presente", "3rd_singular")
        == "se levanta"
    )
    assert (
        gen.generate("levantarse", "indicativo_presente", "1st_plural")
        == "nos levantamos"
    )
    assert (
        gen.generate("levantarse", "indicativo_presente", "2nd_plural")
        == "os levantáis"
    )
    assert (
        gen.generate("levantarse", "indicativo_presente", "3rd_plural") == "se levantan"
    )

    # Indicativo pretérito
    assert (
        gen.generate("levantarse", "indicativo_preterito", "1st_singular")
        == "me levanté"
    )
    assert (
        gen.generate("levantarse", "indicativo_preterito", "2nd_singular")
        == "te levantaste"
    )
    assert (
        gen.generate("levantarse", "indicativo_preterito", "3rd_singular")
        == "se levantó"
    )
    assert (
        gen.generate("levantarse", "indicativo_preterito", "1st_plural")
        == "nos levantamos"
    )
    assert (
        gen.generate("levantarse", "indicativo_preterito", "2nd_plural")
        == "os levantasteis"
    )
    assert (
        gen.generate("levantarse", "indicativo_preterito", "3rd_plural")
        == "se levantaron"
    )

    # Indicativo imperfecto
    assert (
        gen.generate("levantarse", "indicativo_imperfecto", "1st_singular")
        == "me levantaba"
    )
    assert (
        gen.generate("levantarse", "indicativo_imperfecto", "2nd_singular")
        == "te levantabas"
    )
    assert (
        gen.generate("levantarse", "indicativo_imperfecto", "3rd_singular")
        == "se levantaba"
    )
    assert (
        gen.generate("levantarse", "indicativo_imperfecto", "1st_plural")
        == "nos levantábamos"
    )
    assert (
        gen.generate("levantarse", "indicativo_imperfecto", "2nd_plural")
        == "os levantabais"
    )
    assert (
        gen.generate("levantarse", "indicativo_imperfecto", "3rd_plural")
        == "se levantaban"
    )

    # Indicativo futuro
    assert (
        gen.generate("levantarse", "indicativo_futuro", "1st_singular")
        == "me levantaré"
    )
    assert (
        gen.generate("levantarse", "indicativo_futuro", "2nd_singular")
        == "te levantarás"
    )
    assert (
        gen.generate("levantarse", "indicativo_futuro", "3rd_singular")
        == "se levantará"
    )
    assert (
        gen.generate("levantarse", "indicativo_futuro", "1st_plural")
        == "nos levantaremos"
    )
    assert (
        gen.generate("levantarse", "indicativo_futuro", "2nd_plural")
        == "os levantaréis"
    )
    assert (
        gen.generate("levantarse", "indicativo_futuro", "3rd_plural") == "se levantarán"
    )

    # Condicional
    assert gen.generate("levantarse", "condicional", "1st_singular") == "me levantaría"
    assert gen.generate("levantarse", "condicional", "2nd_singular") == "te levantarías"
    assert gen.generate("levantarse", "condicional", "3rd_singular") == "se levantaría"
    assert (
        gen.generate("levantarse", "condicional", "1st_plural") == "nos levantaríamos"
    )
    assert gen.generate("levantarse", "condicional", "2nd_plural") == "os levantaríais"
    assert gen.generate("levantarse", "condicional", "3rd_plural") == "se levantarían"

    # Subjuntivo presente
    assert (
        gen.generate("levantarse", "subjuntivo_presente", "1st_singular")
        == "me levante"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_presente", "2nd_singular")
        == "te levantes"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_presente", "3rd_singular")
        == "se levante"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_presente", "1st_plural")
        == "nos levantemos"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_presente", "2nd_plural")
        == "os levantéis"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_presente", "3rd_plural") == "se levanten"
    )

    # Subjuntivo imperfecto
    assert (
        gen.generate("levantarse", "subjuntivo_imperfecto", "1st_singular")
        == "me levantara"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_imperfecto", "2nd_singular")
        == "te levantaras"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_imperfecto", "3rd_singular")
        == "se levantara"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_imperfecto", "1st_plural")
        == "nos levantáramos"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_imperfecto", "2nd_plural")
        == "os levantarais"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_imperfecto", "3rd_plural")
        == "se levantaran"
    )

    # Subjuntivo futuro
    assert (
        gen.generate("levantarse", "subjuntivo_futuro", "1st_singular")
        == "me levantare"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_futuro", "2nd_singular")
        == "te levantares"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_futuro", "3rd_singular")
        == "se levantare"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_futuro", "1st_plural")
        == "nos levantáremos"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_futuro", "2nd_plural")
        == "os levantareis"
    )
    assert (
        gen.generate("levantarse", "subjuntivo_futuro", "3rd_plural") == "se levantaren"
    )

    # Imperativo afirmativo (no 1st person singular)
    assert (
        gen.generate("levantarse", "imperativo_affirmativo", "2nd_singular")
        == "levántate"
    )
    assert (
        gen.generate("levantarse", "imperativo_affirmativo", "3rd_singular")
        == "levántese"
    )
    assert (
        gen.generate("levantarse", "imperativo_affirmativo", "1st_plural")
        == "levantémonos"
    )
    assert (
        gen.generate("levantarse", "imperativo_affirmativo", "2nd_plural")
        == "levantaos"
    )
    assert (
        gen.generate("levantarse", "imperativo_affirmativo", "3rd_plural")
        == "levántense"
    )

    # Imperativo negativo (no 1st person singular)
    assert (
        gen.generate("levantarse", "imperativo_negativo", "2nd_singular")
        == "no te levantes"
    )
    assert (
        gen.generate("levantarse", "imperativo_negativo", "3rd_singular")
        == "no se levante"
    )
    assert (
        gen.generate("levantarse", "imperativo_negativo", "1st_plural")
        == "no nos levantemos"
    )
    assert (
        gen.generate("levantarse", "imperativo_negativo", "2nd_plural")
        == "no os levantéis"
    )
    assert (
        gen.generate("levantarse", "imperativo_negativo", "3rd_plural")
        == "no se levanten"
    )


def test_reírse():
    # Non-personal forms
    assert gen.generate("reírse", "infinitivo", "not_applicable") == "reírse"
    assert gen.generate("reírse", "gerundio", "not_applicable") == "reiéndose"
    assert gen.generate("reírse", "participio", "not_applicable") == ""

    # Indicativo presente
    assert gen.generate("reírse", "indicativo_presente", "1st_singular") == "me reo"
    assert gen.generate("reírse", "indicativo_presente", "2nd_singular") == "te rees"
    assert gen.generate("reírse", "indicativo_presente", "3rd_singular") == "se ree"
    assert gen.generate("reírse", "indicativo_presente", "1st_plural") == "nos reimos"
    assert gen.generate("reírse", "indicativo_presente", "2nd_plural") == "os reís"
    assert gen.generate("reírse", "indicativo_presente", "3rd_plural") == "se reen"

    # Indicativo pretérito
    assert gen.generate("reírse", "indicativo_preterito", "1st_singular") == "me reí"
    assert gen.generate("reírse", "indicativo_preterito", "2nd_singular") == "te reiste"
    assert gen.generate("reírse", "indicativo_preterito", "3rd_singular") == "se reió"
    assert gen.generate("reírse", "indicativo_preterito", "1st_plural") == "nos reimos"
    assert gen.generate("reírse", "indicativo_preterito", "2nd_plural") == "os reisteis"
    assert gen.generate("reírse", "indicativo_preterito", "3rd_plural") == "se reieron"

    # Indicativo imperfecto
    assert gen.generate("reírse", "indicativo_imperfecto", "1st_singular") == "me reía"
    assert gen.generate("reírse", "indicativo_imperfecto", "2nd_singular") == "te reías"
    assert gen.generate("reírse", "indicativo_imperfecto", "3rd_singular") == "se reía"
    assert (
        gen.generate("reírse", "indicativo_imperfecto", "1st_plural") == "nos reíamos"
    )
    assert gen.generate("reírse", "indicativo_imperfecto", "2nd_plural") == "os reíais"
    assert gen.generate("reírse", "indicativo_imperfecto", "3rd_plural") == "se reían"

    # Indicativo futuro
    assert gen.generate("reírse", "indicativo_futuro", "1st_singular") == "me reíré"
    assert gen.generate("reírse", "indicativo_futuro", "2nd_singular") == "te reírás"
    assert gen.generate("reírse", "indicativo_futuro", "3rd_singular") == "se reírá"
    assert gen.generate("reírse", "indicativo_futuro", "1st_plural") == "nos reíremos"
    assert gen.generate("reírse", "indicativo_futuro", "2nd_plural") == "os reíréis"
    assert gen.generate("reírse", "indicativo_futuro", "3rd_plural") == "se reírán"

    # Condicional
    assert gen.generate("reírse", "condicional", "1st_singular") == "me reíría"
    assert gen.generate("reírse", "condicional", "2nd_singular") == "te reírías"
    assert gen.generate("reírse", "condicional", "3rd_singular") == "se reíría"
    assert gen.generate("reírse", "condicional", "1st_plural") == "nos reíríamos"
    assert gen.generate("reírse", "condicional", "2nd_plural") == "os reíríais"
    assert gen.generate("reírse", "condicional", "3rd_plural") == "se reírían"

    # Subjuntivo presente
    assert gen.generate("reírse", "subjuntivo_presente", "1st_singular") == "me rea"
    assert gen.generate("reírse", "subjuntivo_presente", "2nd_singular") == "te reas"
    assert gen.generate("reírse", "subjuntivo_presente", "3rd_singular") == "se rea"
    assert gen.generate("reírse", "subjuntivo_presente", "1st_plural") == "nos reamos"
    assert gen.generate("reírse", "subjuntivo_presente", "2nd_plural") == "os reáis"
    assert gen.generate("reírse", "subjuntivo_presente", "3rd_plural") == "se rean"

    # Subjuntivo imperfecto
    assert (
        gen.generate("reírse", "subjuntivo_imperfecto", "1st_singular") == "me reiera"
    )
    assert (
        gen.generate("reírse", "subjuntivo_imperfecto", "2nd_singular") == "te reieras"
    )
    assert (
        gen.generate("reírse", "subjuntivo_imperfecto", "3rd_singular") == "se reiera"
    )
    assert (
        gen.generate("reírse", "subjuntivo_imperfecto", "1st_plural") == "nos reiéramos"
    )
    assert (
        gen.generate("reírse", "subjuntivo_imperfecto", "2nd_plural") == "os reierais"
    )
    assert gen.generate("reírse", "subjuntivo_imperfecto", "3rd_plural") == "se reieran"

    # Subjuntivo futuro
    assert gen.generate("reírse", "subjuntivo_futuro", "1st_singular") == "me reiere"
    assert gen.generate("reírse", "subjuntivo_futuro", "2nd_singular") == "te reieres"
    assert gen.generate("reírse", "subjuntivo_futuro", "3rd_singular") == "se reiere"
    assert gen.generate("reírse", "subjuntivo_futuro", "1st_plural") == "nos reiéremos"
    assert gen.generate("reírse", "subjuntivo_futuro", "2nd_plural") == "os reiereis"
    assert gen.generate("reírse", "subjuntivo_futuro", "3rd_plural") == "se reieren"

    # Imperativo afirmativo (no 1st person singular)
    assert gen.generate("reírse", "imperativo_affirmativo", "2nd_singular") == "ríete"
    assert gen.generate("reírse", "imperativo_affirmativo", "3rd_singular") == "ríase"
    assert gen.generate("reírse", "imperativo_affirmativo", "1st_plural") == "riámonos"
    assert gen.generate("reírse", "imperativo_affirmativo", "2nd_plural") == "reíos"
    assert gen.generate("reírse", "imperativo_affirmativo", "3rd_plural") == "ríanse"

    # Imperativo negativo (no 1st person singular)
    assert gen.generate("reírse", "imperativo_negativo", "2nd_singular") == "no te reas"
    assert gen.generate("reírse", "imperativo_negativo", "3rd_singular") == "no se rea"
    assert (
        gen.generate("reírse", "imperativo_negativo", "1st_plural") == "no nos reamos"
    )
    assert gen.generate("reírse", "imperativo_negativo", "2nd_plural") == "no os reáis"
    assert gen.generate("reírse", "imperativo_negativo", "3rd_plural") == "no se rean"


def test_irse():
    # Non-personal forms
    assert gen.generate("irse", "infinitivo", "not_applicable") == "irse"
    assert gen.generate("irse", "gerundio", "not_applicable") == "iéndose"
    assert gen.generate("irse", "participio", "not_applicable") == ""

    # Indicativo presente
    assert gen.generate("irse", "indicativo_presente", "1st_singular") == "me o"
    assert gen.generate("irse", "indicativo_presente", "2nd_singular") == "te es"
    assert gen.generate("irse", "indicativo_presente", "3rd_singular") == "se e"
    assert gen.generate("irse", "indicativo_presente", "1st_plural") == "nos imos"
    assert gen.generate("irse", "indicativo_presente", "2nd_plural") == "os ís"
    assert gen.generate("irse", "indicativo_presente", "3rd_plural") == "se en"

    # Indicativo pretérito
    assert gen.generate("irse", "indicativo_preterito", "1st_singular") == "me í"
    assert gen.generate("irse", "indicativo_preterito", "2nd_singular") == "te iste"
    assert gen.generate("irse", "indicativo_preterito", "3rd_singular") == "se ió"
    assert gen.generate("irse", "indicativo_preterito", "1st_plural") == "nos imos"
    assert gen.generate("irse", "indicativo_preterito", "2nd_plural") == "os isteis"
    assert gen.generate("irse", "indicativo_preterito", "3rd_plural") == "se ieron"

    # Indicativo imperfecto
    assert gen.generate("irse", "indicativo_imperfecto", "1st_singular") == "me ía"
    assert gen.generate("irse", "indicativo_imperfecto", "2nd_singular") == "te ías"
    assert gen.generate("irse", "indicativo_imperfecto", "3rd_singular") == "se ía"
    assert gen.generate("irse", "indicativo_imperfecto", "1st_plural") == "nos íamos"
    assert gen.generate("irse", "indicativo_imperfecto", "2nd_plural") == "os íais"
    assert gen.generate("irse", "indicativo_imperfecto", "3rd_plural") == "se ían"

    # Indicativo futuro
    assert gen.generate("irse", "indicativo_futuro", "1st_singular") == "me iré"
    assert gen.generate("irse", "indicativo_futuro", "2nd_singular") == "te irás"
    assert gen.generate("irse", "indicativo_futuro", "3rd_singular") == "se irá"
    assert gen.generate("irse", "indicativo_futuro", "1st_plural") == "nos iremos"
    assert gen.generate("irse", "indicativo_futuro", "2nd_plural") == "os iréis"
    assert gen.generate("irse", "indicativo_futuro", "3rd_plural") == "se irán"

    # Condicional
    assert gen.generate("irse", "condicional", "1st_singular") == "me iría"
    assert gen.generate("irse", "condicional", "2nd_singular") == "te irías"
    assert gen.generate("irse", "condicional", "3rd_singular") == "se iría"
    assert gen.generate("irse", "condicional", "1st_plural") == "nos iríamos"
    assert gen.generate("irse", "condicional", "2nd_plural") == "os iríais"
    assert gen.generate("irse", "condicional", "3rd_plural") == "se irían"

    # Subjuntivo presente
    assert gen.generate("irse", "subjuntivo_presente", "1st_singular") == "me a"
    assert gen.generate("irse", "subjuntivo_presente", "2nd_singular") == "te as"
    assert gen.generate("irse", "subjuntivo_presente", "3rd_singular") == "se a"
    assert gen.generate("irse", "subjuntivo_presente", "1st_plural") == "nos amos"
    assert gen.generate("irse", "subjuntivo_presente", "2nd_plural") == "os áis"
    assert gen.generate("irse", "subjuntivo_presente", "3rd_plural") == "se an"

    # Subjuntivo imperfecto
    assert gen.generate("irse", "subjuntivo_imperfecto", "1st_singular") == "me iera"
    assert gen.generate("irse", "subjuntivo_imperfecto", "2nd_singular") == "te ieras"
    assert gen.generate("irse", "subjuntivo_imperfecto", "3rd_singular") == "se iera"
    assert gen.generate("irse", "subjuntivo_imperfecto", "1st_plural") == "nos iéramos"
    assert gen.generate("irse", "subjuntivo_imperfecto", "2nd_plural") == "os ierais"
    assert gen.generate("irse", "subjuntivo_imperfecto", "3rd_plural") == "se ieran"

    # Subjuntivo futuro
    assert gen.generate("irse", "subjuntivo_futuro", "1st_singular") == "me iere"
    assert gen.generate("irse", "subjuntivo_futuro", "2nd_singular") == "te ieres"
    assert gen.generate("irse", "subjuntivo_futuro", "3rd_singular") == "se iere"
    assert gen.generate("irse", "subjuntivo_futuro", "1st_plural") == "nos iéremos"
    assert gen.generate("irse", "subjuntivo_futuro", "2nd_plural") == "os iereis"
    assert gen.generate("irse", "subjuntivo_futuro", "3rd_plural") == "se ieren"

    # Imperativo afirmativo (no 1st person singular)
    assert gen.generate("irse", "imperativo_affirmativo", "2nd_singular") == "vete"
    assert gen.generate("irse", "imperativo_affirmativo", "3rd_singular") == "váyase"
    assert gen.generate("irse", "imperativo_affirmativo", "1st_plural") == "vámonos"
    assert gen.generate("irse", "imperativo_affirmativo", "2nd_plural") == "idos"
    assert gen.generate("irse", "imperativo_affirmativo", "3rd_plural") == "váyanse"

    # Imperativo negativo (no 1st person singular)
    assert gen.generate("irse", "imperativo_negativo", "2nd_singular") == "no te as"
    assert gen.generate("irse", "imperativo_negativo", "3rd_singular") == "no se a"
    assert gen.generate("irse", "imperativo_negativo", "1st_plural") == "no nos amos"
    assert gen.generate("irse", "imperativo_negativo", "2nd_plural") == "no os áis"
    assert gen.generate("irse", "imperativo_negativo", "3rd_plural") == "no se an"


def test_meterse():
    # Non-personal forms
    assert gen.generate("meterse", "infinitivo", "not_applicable") == "meterse"
    assert gen.generate("meterse", "gerundio", "not_applicable") == "metiéndose"
    assert gen.generate("meterse", "participio", "not_applicable") == ""

    # Indicativo presente
    assert gen.generate("meterse", "indicativo_presente", "1st_singular") == "me meto"
    assert gen.generate("meterse", "indicativo_presente", "2nd_singular") == "te metes"
    assert gen.generate("meterse", "indicativo_presente", "3rd_singular") == "se mete"
    assert gen.generate("meterse", "indicativo_presente", "1st_plural") == "nos metemos"
    assert gen.generate("meterse", "indicativo_presente", "2nd_plural") == "os metéis"
    assert gen.generate("meterse", "indicativo_presente", "3rd_plural") == "se meten"

    # Indicativo pretérito
    assert gen.generate("meterse", "indicativo_preterito", "1st_singular") == "me metí"
    assert (
        gen.generate("meterse", "indicativo_preterito", "2nd_singular") == "te metiste"
    )
    assert gen.generate("meterse", "indicativo_preterito", "3rd_singular") == "se metió"
    assert (
        gen.generate("meterse", "indicativo_preterito", "1st_plural") == "nos metimos"
    )
    assert (
        gen.generate("meterse", "indicativo_preterito", "2nd_plural") == "os metisteis"
    )
    assert (
        gen.generate("meterse", "indicativo_preterito", "3rd_plural") == "se metieron"
    )

    # Indicativo imperfecto
    assert (
        gen.generate("meterse", "indicativo_imperfecto", "1st_singular") == "me metía"
    )
    assert (
        gen.generate("meterse", "indicativo_imperfecto", "2nd_singular") == "te metías"
    )
    assert (
        gen.generate("meterse", "indicativo_imperfecto", "3rd_singular") == "se metía"
    )
    assert (
        gen.generate("meterse", "indicativo_imperfecto", "1st_plural") == "nos metíamos"
    )
    assert (
        gen.generate("meterse", "indicativo_imperfecto", "2nd_plural") == "os metíais"
    )
    assert gen.generate("meterse", "indicativo_imperfecto", "3rd_plural") == "se metían"

    # Indicativo futuro
    assert gen.generate("meterse", "indicativo_futuro", "1st_singular") == "me meteré"
    assert gen.generate("meterse", "indicativo_futuro", "2nd_singular") == "te meterás"
    assert gen.generate("meterse", "indicativo_futuro", "3rd_singular") == "se meterá"
    assert gen.generate("meterse", "indicativo_futuro", "1st_plural") == "nos meteremos"
    assert gen.generate("meterse", "indicativo_futuro", "2nd_plural") == "os meteréis"
    assert gen.generate("meterse", "indicativo_futuro", "3rd_plural") == "se meterán"

    # Condicional
    assert gen.generate("meterse", "condicional", "1st_singular") == "me metería"
    assert gen.generate("meterse", "condicional", "2nd_singular") == "te meterías"
    assert gen.generate("meterse", "condicional", "3rd_singular") == "se metería"
    assert gen.generate("meterse", "condicional", "1st_plural") == "nos meteríamos"
    assert gen.generate("meterse", "condicional", "2nd_plural") == "os meteríais"
    assert gen.generate("meterse", "condicional", "3rd_plural") == "se meterían"

    # Subjuntivo presente
    assert gen.generate("meterse", "subjuntivo_presente", "1st_singular") == "me meta"
    assert gen.generate("meterse", "subjuntivo_presente", "2nd_singular") == "te metas"
    assert gen.generate("meterse", "subjuntivo_presente", "3rd_singular") == "se meta"
    assert gen.generate("meterse", "subjuntivo_presente", "1st_plural") == "nos metamos"
    assert gen.generate("meterse", "subjuntivo_presente", "2nd_plural") == "os metáis"
    assert gen.generate("meterse", "subjuntivo_presente", "3rd_plural") == "se metan"

    # Subjuntivo imperfecto
    assert (
        gen.generate("meterse", "subjuntivo_imperfecto", "1st_singular") == "me metiera"
    )
    assert (
        gen.generate("meterse", "subjuntivo_imperfecto", "2nd_singular")
        == "te metieras"
    )
    assert (
        gen.generate("meterse", "subjuntivo_imperfecto", "3rd_singular") == "se metiera"
    )
    assert (
        gen.generate("meterse", "subjuntivo_imperfecto", "1st_plural")
        == "nos metiéramos"
    )
    assert (
        gen.generate("meterse", "subjuntivo_imperfecto", "2nd_plural") == "os metierais"
    )
    assert (
        gen.generate("meterse", "subjuntivo_imperfecto", "3rd_plural") == "se metieran"
    )

    # Subjuntivo futuro
    assert gen.generate("meterse", "subjuntivo_futuro", "1st_singular") == "me metiere"
    assert gen.generate("meterse", "subjuntivo_futuro", "2nd_singular") == "te metieres"
    assert gen.generate("meterse", "subjuntivo_futuro", "3rd_singular") == "se metiere"
    assert (
        gen.generate("meterse", "subjuntivo_futuro", "1st_plural") == "nos metiéremos"
    )
    assert gen.generate("meterse", "subjuntivo_futuro", "2nd_plural") == "os metiereis"
    assert gen.generate("meterse", "subjuntivo_futuro", "3rd_plural") == "se metieren"

    # Imperativo afirmativo (no 1st person singular)
    assert gen.generate("meterse", "imperativo_affirmativo", "2nd_singular") == "métete"
    assert gen.generate("meterse", "imperativo_affirmativo", "3rd_singular") == "métase"
    assert (
        gen.generate("meterse", "imperativo_affirmativo", "1st_plural") == "metámonos"
    )
    assert gen.generate("meterse", "imperativo_affirmativo", "2nd_plural") == "meteos"
    assert gen.generate("meterse", "imperativo_affirmativo", "3rd_plural") == "métanse"

    # Imperativo negativo (no 1st person singular)
    assert (
        gen.generate("meterse", "imperativo_negativo", "2nd_singular") == "no te metas"
    )
    assert (
        gen.generate("meterse", "imperativo_negativo", "3rd_singular") == "no se meta"
    )
    assert (
        gen.generate("meterse", "imperativo_negativo", "1st_plural") == "no nos metamos"
    )
    assert (
        gen.generate("meterse", "imperativo_negativo", "2nd_plural") == "no os metáis"
    )
    assert gen.generate("meterse", "imperativo_negativo", "3rd_plural") == "no se metan"
