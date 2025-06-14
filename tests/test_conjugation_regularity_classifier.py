import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utilities.conjugation_regularity_classifier import (
    ConjugationRegularityClassifier,
)

classifier = ConjugationRegularityClassifier()


def test_regular():
    forms = {"indicativo_presente": {"1st_singular": "hablo"}}
    assert classifier.classify("hablar", forms) == "regular"


def test_morphological_irregular():
    forms = {"indicativo_presente": {"1st_singular": "pienso"}}
    assert classifier.classify("pensar", forms) == "morphologically_irregular"


def test_c_to_qu():
    forms = {"indicativo_preterito": {"1st_singular": "busqué"}}
    assert classifier.classify("buscar", forms) == "orthographically_irregular"


def test_g_to_gu():
    forms = {"indicativo_preterito": {"1st_singular": "llegué"}}
    assert classifier.classify("llegar", forms) == "orthographically_irregular"


def test_z_to_c():
    forms = {"indicativo_preterito": {"1st_singular": "empecé"}}
    assert classifier.classify("empezar", forms) == "orthographically_irregular"


def test_g_to_j():
    forms = {"indicativo_presente": {"1st_singular": "protejo"}}
    assert classifier.classify("proteger", forms) == "orthographically_irregular"


def test_gu_to_gue_dieresis():
    forms = {"indicativo_preterito": {"1st_singular": "averigüé"}}
    assert classifier.classify("averiguar", forms) == "orthographically_irregular"


def test_guir_drop_u():
    forms = {"indicativo_presente": {"1st_singular": "distingo"}}
    assert classifier.classify("distinguir", forms) == "orthographically_irregular"


def test_c_to_z_after_consonant():
    forms = {"indicativo_presente": {"1st_singular": "venzo"}}
    assert classifier.classify("vencer", forms) == "orthographically_irregular"


def test_i_to_y():
    forms = {"indicativo_preterito": {"3rd_singular": "leyó"}}
    assert classifier.classify("leer", forms) == "orthographically_irregular"


def test_written_accent_shift():
    forms = {"indicativo_presente": {"1st_singular": "envío"}}
    assert classifier.classify("enviar", forms) == "orthographically_irregular"
