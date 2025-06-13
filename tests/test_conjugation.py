import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from regular_form_generator import RegularFormGenerator

gen = RegularFormGenerator()

FORMS = list(gen.FORM_NAME_TO_ID.keys())
PERSONS = list(gen.PERSON_NAME_TO_ID.keys())


def _check_all_combos(verb):
    reflexive = verb.endswith("se")
    for form in FORMS:
        for person in PERSONS:
            result = gen.generate(verb, form, person)
            if form == "participio":
                if reflexive:
                    assert result == ""
                else:
                    assert result != ""
            elif form in ["infinitivo", "gerundio"]:
                assert result != ""
            elif form in ["imperativo_affirmativo", "imperativo_negativo"]:
                if person in ["not_applicable", "1st_singular"]:
                    assert result == ""
                else:
                    assert result != ""
            else:
                if person == "not_applicable":
                    assert result == ""
                else:
                    assert result != ""


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
    
    _check_all_combos("hablar")


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
    
    _check_all_combos("deber")


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
    
    _check_all_combos("vivir")


def test_oír():
    assert gen.generate("oír", "indicativo_presente", "1st_singular") == "oo"
    assert gen.generate("oír", "indicativo_preterito", "3rd_singular") == "oió"
    assert gen.generate("oír", "gerundio", "not_applicable") == "oiendo"
    assert gen.generate("oír", "participio", "not_applicable") == "oido"
    _check_all_combos("oír")


def test_levantarse():
    assert (
        gen.generate("levantarse", "indicativo_presente", "1st_singular")
        == "me levanto"
    )
    assert gen.generate("levantarse", "gerundio", "not_applicable") == "levantándose"
    assert (
        gen.generate("levantarse", "imperativo_affirmativo", "2nd_plural")
        == "levantaos"
    )
    assert (
        gen.generate("levantarse", "imperativo_negativo", "2nd_singular")
        == "no te levantes"
    )
    _check_all_combos("levantarse")


def test_reírse():
    assert gen.generate("reírse", "indicativo_presente", "1st_singular") == "me reo"
    assert gen.generate("reírse", "gerundio", "not_applicable") == "reiéndose"
    assert gen.generate("reírse", "imperativo_affirmativo", "2nd_plural") == "reíos"
    assert gen.generate("reírse", "imperativo_affirmativo", "2nd_singular") == "reete"
    assert gen.generate("reírse", "imperativo_negativo", "2nd_singular") == "no te reas"
    _check_all_combos("reírse")


def test_irse():
    assert gen.generate("irse", "indicativo_presente", "1st_singular") == "me o"
    assert gen.generate("irse", "imperativo_affirmativo", "2nd_plural") == "idos"
    assert gen.generate("irse", "imperativo_negativo", "2nd_plural") == "no os áis"
    _check_all_combos("irse")


def test_meterse():
    assert gen.generate("meterse", "indicativo_presente", "3rd_singular") == "se mete"
    assert gen.generate("meterse", "imperativo_affirmativo", "2nd_plural") == "meteos"
    assert (
        gen.generate("meterse", "imperativo_negativo", "2nd_singular") == "no te metas"
    )
    _check_all_combos("meterse")
