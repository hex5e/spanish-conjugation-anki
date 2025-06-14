import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utilities.get_conjugation_rae import RAEConjugationFetcher
from utilities.get_conjugation_rae import RAEConjugationTransformer
from utilities.get_conjugation_rae import strip_reflexive


def test_meterse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("meterse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("meterse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["infinitivo"] == "meterse"
    assert out["gerundio"] == "metiéndose"
    assert out["participio"] == ""

    # Indicativo presente
    assert out["indicativo_presente"]["1st_singular"] == "me meto"
    assert out["indicativo_presente"]["2nd_singular"] == "te metes"
    assert out["indicativo_presente"]["3rd_singular"] == "se mete"
    assert out["indicativo_presente"]["1st_plural"] == "nos metemos"
    assert out["indicativo_presente"]["2nd_plural"] == "os metéis"
    assert out["indicativo_presente"]["3rd_plural"] == "se meten"

    # Indicativo pretérito
    assert out["indicativo_preterito"]["1st_singular"] == "me metí"
    assert out["indicativo_preterito"]["2nd_singular"] == "te metiste"
    assert out["indicativo_preterito"]["3rd_singular"] == "se metió"
    assert out["indicativo_preterito"]["1st_plural"] == "nos metimos"
    assert out["indicativo_preterito"]["2nd_plural"] == "os metisteis"
    assert out["indicativo_preterito"]["3rd_plural"] == "se metieron"

    # Indicativo imperfecto
    assert out["indicativo_imperfecto"]["1st_singular"] == "me metía"
    assert out["indicativo_imperfecto"]["2nd_singular"] == "te metías"
    assert out["indicativo_imperfecto"]["3rd_singular"] == "se metía"
    assert out["indicativo_imperfecto"]["1st_plural"] == "nos metíamos"
    assert out["indicativo_imperfecto"]["2nd_plural"] == "os metíais"
    assert out["indicativo_imperfecto"]["3rd_plural"] == "se metían"

    # Indicativo futuro
    assert out["indicativo_futuro"]["1st_singular"] == "me meteré"
    assert out["indicativo_futuro"]["2nd_singular"] == "te meterás"
    assert out["indicativo_futuro"]["3rd_singular"] == "se meterá"
    assert out["indicativo_futuro"]["1st_plural"] == "nos meteremos"
    assert out["indicativo_futuro"]["2nd_plural"] == "os meteréis"
    assert out["indicativo_futuro"]["3rd_plural"] == "se meterán"

    # Condicional
    assert out["condicional"]["1st_singular"] == "me metería"
    assert out["condicional"]["2nd_singular"] == "te meterías"
    assert out["condicional"]["3rd_singular"] == "se metería"
    assert out["condicional"]["1st_plural"] == "nos meteríamos"
    assert out["condicional"]["2nd_plural"] == "os meteríais"
    assert out["condicional"]["3rd_plural"] == "se meterían"

    # Subjuntivo presente
    assert out["subjuntivo_presente"]["1st_singular"] == "me meta"
    assert out["subjuntivo_presente"]["2nd_singular"] == "te metas"
    assert out["subjuntivo_presente"]["3rd_singular"] == "se meta"
    assert out["subjuntivo_presente"]["1st_plural"] == "nos metamos"
    assert out["subjuntivo_presente"]["2nd_plural"] == "os metáis"
    assert out["subjuntivo_presente"]["3rd_plural"] == "se metan"

    # Subjuntivo imperfecto
    assert out["subjuntivo_imperfecto"]["1st_singular"] == "me metiera"
    assert out["subjuntivo_imperfecto"]["2nd_singular"] == "te metieras"
    assert out["subjuntivo_imperfecto"]["3rd_singular"] == "se metiera"
    assert out["subjuntivo_imperfecto"]["1st_plural"] == "nos metiéramos"
    assert out["subjuntivo_imperfecto"]["2nd_plural"] == "os metierais"
    assert out["subjuntivo_imperfecto"]["3rd_plural"] == "se metieran"

    # Subjuntivo futuro
    assert out["subjuntivo_futuro"]["1st_singular"] == "me metiere"
    assert out["subjuntivo_futuro"]["2nd_singular"] == "te metieres"
    assert out["subjuntivo_futuro"]["3rd_singular"] == "se metiere"
    assert out["subjuntivo_futuro"]["1st_plural"] == "nos metiéremos"
    assert out["subjuntivo_futuro"]["2nd_plural"] == "os metiereis"
    assert out["subjuntivo_futuro"]["3rd_plural"] == "se metieren"

    # Imperativo afirmativo
    assert out["imperativo_affirmativo"]["2nd_singular"] == "métete"
    assert out["imperativo_affirmativo"]["3rd_singular"] == "métase"
    assert out["imperativo_affirmativo"]["1st_plural"] == "metámonos"
    assert out["imperativo_affirmativo"]["2nd_plural"] == "meteos"
    assert out["imperativo_affirmativo"]["3rd_plural"] == "métanse"

    # Imperativo negativo
    assert out["imperativo_negativo"]["2nd_singular"] == "no te metas"
    assert out["imperativo_negativo"]["3rd_singular"] == "no se meta"
    assert out["imperativo_negativo"]["1st_plural"] == "no nos metamos"
    assert out["imperativo_negativo"]["2nd_plural"] == "no os metáis"
    assert out["imperativo_negativo"]["3rd_plural"] == "no se metan"


def test_arrepentirse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("arrepentirse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("arrepentirse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["infinitivo"] == "arrepentirse"
    assert out["gerundio"] == "arrepintiéndose"
    assert out["participio"] == ""

    # Indicativo presente
    assert out["indicativo_presente"]["1st_singular"] == "me arrepiento"
    assert out["indicativo_presente"]["2nd_singular"] == "te arrepientes"
    assert out["indicativo_presente"]["3rd_singular"] == "se arrepiente"
    assert out["indicativo_presente"]["1st_plural"] == "nos arrepentimos"
    assert out["indicativo_presente"]["2nd_plural"] == "os arrepentís"
    assert out["indicativo_presente"]["3rd_plural"] == "se arrepienten"

    # Indicativo pretérito
    assert out["indicativo_preterito"]["1st_singular"] == "me arrepentí"
    assert out["indicativo_preterito"]["2nd_singular"] == "te arrepentiste"
    assert out["indicativo_preterito"]["3rd_singular"] == "se arrepintió"
    assert out["indicativo_preterito"]["1st_plural"] == "nos arrepentimos"
    assert out["indicativo_preterito"]["2nd_plural"] == "os arrepentisteis"
    assert out["indicativo_preterito"]["3rd_plural"] == "se arrepintieron"

    # Indicativo imperfecto
    assert out["indicativo_imperfecto"]["1st_singular"] == "me arrepentía"
    assert out["indicativo_imperfecto"]["2nd_singular"] == "te arrepentías"
    assert out["indicativo_imperfecto"]["3rd_singular"] == "se arrepentía"
    assert out["indicativo_imperfecto"]["1st_plural"] == "nos arrepentíamos"
    assert out["indicativo_imperfecto"]["2nd_plural"] == "os arrepentíais"
    assert out["indicativo_imperfecto"]["3rd_plural"] == "se arrepentían"

    # Indicativo futuro
    assert out["indicativo_futuro"]["1st_singular"] == "me arrepentiré"
    assert out["indicativo_futuro"]["2nd_singular"] == "te arrepentirás"
    assert out["indicativo_futuro"]["3rd_singular"] == "se arrepentirá"
    assert out["indicativo_futuro"]["1st_plural"] == "nos arrepentiremos"
    assert out["indicativo_futuro"]["2nd_plural"] == "os arrepentiréis"
    assert out["indicativo_futuro"]["3rd_plural"] == "se arrepentirán"

    # Condicional
    assert out["condicional"]["1st_singular"] == "me arrepentiría"
    assert out["condicional"]["2nd_singular"] == "te arrepentirías"
    assert out["condicional"]["3rd_singular"] == "se arrepentiría"
    assert out["condicional"]["1st_plural"] == "nos arrepentiríamos"
    assert out["condicional"]["2nd_plural"] == "os arrepentiríais"
    assert out["condicional"]["3rd_plural"] == "se arrepentirían"

    # Subjuntivo presente
    assert out["subjuntivo_presente"]["1st_singular"] == "me arrepienta"
    assert out["subjuntivo_presente"]["2nd_singular"] == "te arrepientas"
    assert out["subjuntivo_presente"]["3rd_singular"] == "se arrepienta"
    assert out["subjuntivo_presente"]["1st_plural"] == "nos arrepintamos"
    assert out["subjuntivo_presente"]["2nd_plural"] == "os arrepintáis"
    assert out["subjuntivo_presente"]["3rd_plural"] == "se arrepientan"

    # Subjuntivo imperfecto
    assert out["subjuntivo_imperfecto"]["1st_singular"] == "me arrepintiera"
    assert out["subjuntivo_imperfecto"]["2nd_singular"] == "te arrepintieras"
    assert out["subjuntivo_imperfecto"]["3rd_singular"] == "se arrepintiera"
    assert out["subjuntivo_imperfecto"]["1st_plural"] == "nos arrepintiéramos"
    assert out["subjuntivo_imperfecto"]["2nd_plural"] == "os arrepintierais"
    assert out["subjuntivo_imperfecto"]["3rd_plural"] == "se arrepintieran"

    # Subjuntivo futuro
    assert out["subjuntivo_futuro"]["1st_singular"] == "me arrepintiere"
    assert out["subjuntivo_futuro"]["2nd_singular"] == "te arrepintieres"
    assert out["subjuntivo_futuro"]["3rd_singular"] == "se arrepintiere"
    assert out["subjuntivo_futuro"]["1st_plural"] == "nos arrepintiéremos"
    assert out["subjuntivo_futuro"]["2nd_plural"] == "os arrepintiereis"
    assert out["subjuntivo_futuro"]["3rd_plural"] == "se arrepintieren"

    # Imperativo afirmativo
    assert out["imperativo_affirmativo"]["2nd_singular"] == "arrepiéntete"
    assert out["imperativo_affirmativo"]["3rd_singular"] == "arrepiéntase"
    assert out["imperativo_affirmativo"]["1st_plural"] == "arrepintámonos"
    assert out["imperativo_affirmativo"]["2nd_plural"] == "arrepentíos"
    assert out["imperativo_affirmativo"]["3rd_plural"] == "arrepiéntanse"

    # Imperativo negativo
    assert out["imperativo_negativo"]["2nd_singular"] == "no te arrepientas"
    assert out["imperativo_negativo"]["3rd_singular"] == "no se arrepienta"
    assert out["imperativo_negativo"]["1st_plural"] == "no nos arrepintamos"
    assert out["imperativo_negativo"]["2nd_plural"] == "no os arrepintáis"
    assert out["imperativo_negativo"]["3rd_plural"] == "no se arrepientan"


def test_irse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("irse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("irse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["infinitivo"] == "irse"
    assert out["gerundio"] == "yéndose"
    assert out["participio"] == ""

    # Indicativo presente
    assert out["indicativo_presente"]["1st_singular"] == "me voy"
    assert out["indicativo_presente"]["2nd_singular"] == "te vas"
    assert out["indicativo_presente"]["3rd_singular"] == "se va"
    assert out["indicativo_presente"]["1st_plural"] == "nos vamos"
    assert out["indicativo_presente"]["2nd_plural"] == "os vais"
    assert out["indicativo_presente"]["3rd_plural"] == "se van"

    # Indicativo pretérito
    assert out["indicativo_preterito"]["1st_singular"] == "me fui"
    assert out["indicativo_preterito"]["2nd_singular"] == "te fuiste"
    assert out["indicativo_preterito"]["3rd_singular"] == "se fue"
    assert out["indicativo_preterito"]["1st_plural"] == "nos fuimos"
    assert out["indicativo_preterito"]["2nd_plural"] == "os fuisteis"
    assert out["indicativo_preterito"]["3rd_plural"] == "se fueron"

    # Indicativo imperfecto
    assert out["indicativo_imperfecto"]["1st_singular"] == "me iba"
    assert out["indicativo_imperfecto"]["2nd_singular"] == "te ibas"
    assert out["indicativo_imperfecto"]["3rd_singular"] == "se iba"
    assert out["indicativo_imperfecto"]["1st_plural"] == "nos íbamos"
    assert out["indicativo_imperfecto"]["2nd_plural"] == "os ibais"
    assert out["indicativo_imperfecto"]["3rd_plural"] == "se iban"

    # Indicativo futuro
    assert out["indicativo_futuro"]["1st_singular"] == "me iré"
    assert out["indicativo_futuro"]["2nd_singular"] == "te irás"
    assert out["indicativo_futuro"]["3rd_singular"] == "se irá"
    assert out["indicativo_futuro"]["1st_plural"] == "nos iremos"
    assert out["indicativo_futuro"]["2nd_plural"] == "os iréis"
    assert out["indicativo_futuro"]["3rd_plural"] == "se irán"

    # Condicional
    assert out["condicional"]["1st_singular"] == "me iría"
    assert out["condicional"]["2nd_singular"] == "te irías"
    assert out["condicional"]["3rd_singular"] == "se iría"
    assert out["condicional"]["1st_plural"] == "nos iríamos"
    assert out["condicional"]["2nd_plural"] == "os iríais"
    assert out["condicional"]["3rd_plural"] == "se irían"

    # Subjuntivo presente
    assert out["subjuntivo_presente"]["1st_singular"] == "me vaya"
    assert out["subjuntivo_presente"]["2nd_singular"] == "te vayas"
    assert out["subjuntivo_presente"]["3rd_singular"] == "se vaya"
    assert out["subjuntivo_presente"]["1st_plural"] == "nos vayamos"
    assert out["subjuntivo_presente"]["2nd_plural"] == "os vayáis"
    assert out["subjuntivo_presente"]["3rd_plural"] == "se vayan"

    # Subjuntivo imperfecto
    assert out["subjuntivo_imperfecto"]["1st_singular"] == "me fuera"
    assert out["subjuntivo_imperfecto"]["2nd_singular"] == "te fueras"
    assert out["subjuntivo_imperfecto"]["3rd_singular"] == "se fuera"
    assert out["subjuntivo_imperfecto"]["1st_plural"] == "nos fuéramos"
    assert out["subjuntivo_imperfecto"]["2nd_plural"] == "os fuerais"
    assert out["subjuntivo_imperfecto"]["3rd_plural"] == "se fueran"

    # Subjuntivo futuro
    assert out["subjuntivo_futuro"]["1st_singular"] == "me fuere"
    assert out["subjuntivo_futuro"]["2nd_singular"] == "te fueres"
    assert out["subjuntivo_futuro"]["3rd_singular"] == "se fuere"
    assert out["subjuntivo_futuro"]["1st_plural"] == "nos fuéremos"
    assert out["subjuntivo_futuro"]["2nd_plural"] == "os fuereis"
    assert out["subjuntivo_futuro"]["3rd_plural"] == "se fueren"

    # Imperativo afirmativo
    assert out["imperativo_affirmativo"]["2nd_singular"] == "vete"
    assert out["imperativo_affirmativo"]["3rd_singular"] == "váyase"
    assert out["imperativo_affirmativo"]["1st_plural"] == "vámonos"
    assert out["imperativo_affirmativo"]["2nd_plural"] == "idos"
    assert out["imperativo_affirmativo"]["3rd_plural"] == "váyanse"

    # Imperativo negativo
    assert out["imperativo_negativo"]["2nd_singular"] == "no te vayas"
    assert out["imperativo_negativo"]["3rd_singular"] == "no se vaya"
    assert out["imperativo_negativo"]["1st_plural"] == "no nos vayamos"
    assert out["imperativo_negativo"]["2nd_plural"] == "no os vayáis"
    assert out["imperativo_negativo"]["3rd_plural"] == "no se vayan"


def test_reírse():
    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive("reírse")
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer("reírse", is_reflexive=is_reflexive)
    out = transformer.transform(raw)

    assert out["infinitivo"] == "reírse"
    assert out["gerundio"] == "riéndose"
    assert out["participio"] == ""

    # Indicativo presente
    assert out["indicativo_presente"]["1st_singular"] == "me río"
    assert out["indicativo_presente"]["2nd_singular"] == "te ríes"
    assert out["indicativo_presente"]["3rd_singular"] == "se ríe"
    assert out["indicativo_presente"]["1st_plural"] == "nos reímos"
    assert out["indicativo_presente"]["2nd_plural"] == "os reís"
    assert out["indicativo_presente"]["3rd_plural"] == "se ríen"

    # Indicativo pretérito
    assert out["indicativo_preterito"]["1st_singular"] == "me reí"
    assert out["indicativo_preterito"]["2nd_singular"] == "te reíste"
    assert out["indicativo_preterito"]["3rd_singular"] == "se rio"
    assert out["indicativo_preterito"]["1st_plural"] == "nos reímos"
    assert out["indicativo_preterito"]["2nd_plural"] == "os reísteis"
    assert out["indicativo_preterito"]["3rd_plural"] == "se rieron"

    # Indicativo imperfecto
    assert out["indicativo_imperfecto"]["1st_singular"] == "me reía"
    assert out["indicativo_imperfecto"]["2nd_singular"] == "te reías"
    assert out["indicativo_imperfecto"]["3rd_singular"] == "se reía"
    assert out["indicativo_imperfecto"]["1st_plural"] == "nos reíamos"
    assert out["indicativo_imperfecto"]["2nd_plural"] == "os reíais"
    assert out["indicativo_imperfecto"]["3rd_plural"] == "se reían"

    # Indicativo futuro
    assert out["indicativo_futuro"]["1st_singular"] == "me reiré"
    assert out["indicativo_futuro"]["2nd_singular"] == "te reirás"
    assert out["indicativo_futuro"]["3rd_singular"] == "se reirá"
    assert out["indicativo_futuro"]["1st_plural"] == "nos reiremos"
    assert out["indicativo_futuro"]["2nd_plural"] == "os reiréis"
    assert out["indicativo_futuro"]["3rd_plural"] == "se reirán"

    # Condicional
    assert out["condicional"]["1st_singular"] == "me reiría"
    assert out["condicional"]["2nd_singular"] == "te reirías"
    assert out["condicional"]["3rd_singular"] == "se reiría"
    assert out["condicional"]["1st_plural"] == "nos reiríamos"
    assert out["condicional"]["2nd_plural"] == "os reiríais"
    assert out["condicional"]["3rd_plural"] == "se reirían"

    # Subjuntivo presente
    assert out["subjuntivo_presente"]["1st_singular"] == "me ría"
    assert out["subjuntivo_presente"]["2nd_singular"] == "te rías"
    assert out["subjuntivo_presente"]["3rd_singular"] == "se ría"
    assert out["subjuntivo_presente"]["1st_plural"] == "nos riamos"
    assert out["subjuntivo_presente"]["2nd_plural"] == "os riais"
    assert out["subjuntivo_presente"]["3rd_plural"] == "se rían"

    # Subjuntivo imperfecto
    assert out["subjuntivo_imperfecto"]["1st_singular"] == "me riera"
    assert out["subjuntivo_imperfecto"]["2nd_singular"] == "te rieras"
    assert out["subjuntivo_imperfecto"]["3rd_singular"] == "se riera"
    assert out["subjuntivo_imperfecto"]["1st_plural"] == "nos riéramos"
    assert out["subjuntivo_imperfecto"]["2nd_plural"] == "os rierais"
    assert out["subjuntivo_imperfecto"]["3rd_plural"] == "se rieran"

    # Subjuntivo futuro
    assert out["subjuntivo_futuro"]["1st_singular"] == "me riere"
    assert out["subjuntivo_futuro"]["2nd_singular"] == "te rieres"
    assert out["subjuntivo_futuro"]["3rd_singular"] == "se riere"
    assert out["subjuntivo_futuro"]["1st_plural"] == "nos riéremos"
    assert out["subjuntivo_futuro"]["2nd_plural"] == "os riereis"
    assert out["subjuntivo_futuro"]["3rd_plural"] == "se rieren"

    # Imperativo afirmativo
    assert out["imperativo_affirmativo"]["2nd_singular"] == "ríete"
    assert out["imperativo_affirmativo"]["3rd_singular"] == "ríase"
    assert out["imperativo_affirmativo"]["1st_plural"] == "riámonos"
    assert out["imperativo_affirmativo"]["2nd_plural"] == "reíos"
    assert out["imperativo_affirmativo"]["3rd_plural"] == "ríanse"

    # Imperativo negativo
    assert out["imperativo_negativo"]["2nd_singular"] == "no te rías"
    assert out["imperativo_negativo"]["3rd_singular"] == "no se ría"
    assert out["imperativo_negativo"]["1st_plural"] == "no nos riamos"
    assert out["imperativo_negativo"]["2nd_plural"] == "no os riais"
    assert out["imperativo_negativo"]["3rd_plural"] == "no se rían"
