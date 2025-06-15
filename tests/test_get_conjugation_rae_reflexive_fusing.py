import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utilities.get_conjugation_rae import RAEConjugationFetcher
from utilities.get_conjugation_rae import RAEConjugationTransformer
from utilities.get_conjugation_rae import strip_reflexive


def test_arrepentirse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("arrepentirse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("arrepentirse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["gerundio"] == "arrepintiéndose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "arrepiéntete"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "arrepiéntase"
    assert out["imperativo_afirmativo"]["1st_plural"] == "arrepintámonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "arrepentíos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "arrepiéntanse"


def test_bajarse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("bajarse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("bajarse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["gerundio"] == "bajándose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "bájate"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "bájese"
    assert out["imperativo_afirmativo"]["1st_plural"] == "bajémonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "bajaos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "bájense"


def test_bañarse():
    fetcher = RAEConjugationFetcher()
    raw = fetcher.get_conjugation("bañar")
    transformer = RAEConjugationTransformer("bañarse", is_reflexive=True)
    out = transformer.transform(raw)

    assert out["gerundio"] == "bañándose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "báñate"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "báñese"
    assert out["imperativo_afirmativo"]["1st_plural"] == "bañémonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "bañaos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "báñense"


def test_darse():
    fetcher = RAEConjugationFetcher()
    raw = fetcher.get_conjugation("dar")
    transformer = RAEConjugationTransformer("darse", is_reflexive=True)
    out = transformer.transform(raw)

    assert out["gerundio"] == "dándose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "date"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "dese"
    assert out["imperativo_afirmativo"]["1st_plural"] == "démonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "daos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "dense"


def test_echarse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("echarse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("echarse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["gerundio"] == "echándose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "échate"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "échese"
    assert out["imperativo_afirmativo"]["1st_plural"] == "echémonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "echaos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "échense"


def test_endeudarse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("endeudarse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("endeudarse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["gerundio"] == "endeudándose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "endéudate"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "endéudese"
    assert out["imperativo_afirmativo"]["1st_plural"] == "endeudémonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "endeudaos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "endéudense"


def test_esforzarse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("esforzarse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("esforzarse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["gerundio"] == "esforzándose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "esfuérzate"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "esfuércese"
    assert out["imperativo_afirmativo"]["1st_plural"] == "esforcémonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "esforzaos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "esfuércense"


def test_fijarse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("fijarse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("fijarse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["gerundio"] == "fijándose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "fíjate"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "fíjese"
    assert out["imperativo_afirmativo"]["1st_plural"] == "fijémonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "fijaos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "fíjense"


def test_irse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("irse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("irse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["gerundio"] == "yéndose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "vete"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "váyase"
    assert out["imperativo_afirmativo"]["1st_plural"] == "vámonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "idos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "váyanse"


def test_levantarse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("levantarse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("levantarse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["gerundio"] == "levantándose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "levántate"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "levántese"
    assert out["imperativo_afirmativo"]["1st_plural"] == "levantémonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "levantaos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "levántense"


def test_liarse():
    fetcher = RAEConjugationFetcher()
    raw = fetcher.get_conjugation("liar")
    transformer = RAEConjugationTransformer("liarse", is_reflexive=True)
    out = transformer.transform(raw)

    assert out["gerundio"] == "liándose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "líate"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "líese"
    assert out["imperativo_afirmativo"]["1st_plural"] == "liémonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "liaos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "líense"


def test_meterse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("meterse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("meterse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["gerundio"] == "metiéndose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "métete"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "métase"
    assert out["imperativo_afirmativo"]["1st_plural"] == "metámonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "meteos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "métanse"


def test_quedarse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("quedarse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("quedarse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["gerundio"] == "quedándose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "quédate"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "quédese"
    assert out["imperativo_afirmativo"]["1st_plural"] == "quedémonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "quedaos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "quédense"


def test_quejarse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("quejarse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("quejarse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["gerundio"] == "quejándose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "quéjate"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "quéjese"
    assert out["imperativo_afirmativo"]["1st_plural"] == "quejémonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "quejaos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "quéjense"


def test_reírse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("reírse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("reírse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["gerundio"] == "riéndose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "ríete"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "ríase"
    assert out["imperativo_afirmativo"]["1st_plural"] == "riámonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "reíos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "ríanse"


def test_subirse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("subirse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("subirse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["gerundio"] == "subiéndose"

    # Imperativo afirmativo
    assert out["imperativo_afirmativo"]["2nd_singular"] == "súbete"
    assert out["imperativo_afirmativo"]["3rd_singular"] == "súbase"
    assert out["imperativo_afirmativo"]["1st_plural"] == "subámonos"
    assert out["imperativo_afirmativo"]["2nd_plural"] == "subíos"
    assert out["imperativo_afirmativo"]["3rd_plural"] == "súbanse"
