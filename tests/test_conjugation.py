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
    assert gen.generate("hablar", "indicativo_presente", "1st_singular") == "hablo"
    assert gen.generate("hablar", "indicativo_preterito", "3rd_plural") == "hablaron"
    assert gen.generate("hablar", "gerundio", "not_applicable") == "hablando"
    assert gen.generate("hablar", "participio", "not_applicable") == "hablado"
    _check_all_combos("hablar")


def test_deber():
    assert gen.generate("deber", "indicativo_presente", "1st_plural") == "debemos"
    assert gen.generate("deber", "indicativo_preterito", "2nd_singular") == "debiste"
    assert gen.generate("deber", "participio", "not_applicable") == "debido"
    assert gen.generate("deber", "imperativo_affirmativo", "2nd_singular") == "debe"
    _check_all_combos("deber")


def test_vivir():
    assert gen.generate("vivir", "indicativo_presente", "3rd_plural") == "viven"
    assert gen.generate("vivir", "indicativo_preterito", "1st_singular") == "viví"
    assert gen.generate("vivir", "gerundio", "not_applicable") == "viviendo"
    assert gen.generate("vivir", "imperativo_affirmativo", "2nd_plural") == "vivid"
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
