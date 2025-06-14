"""Fetch Spanish verb conjugations from the RAE dictionary website.

This script scrapes the conjugation tables from ``dle.rae.es``.  The
site sits behind Cloudflare so ``cloudscraper`` is used to emulate a
real browser.  Parsed results are transformed into the deck's JSON
format and printed to stdout.

Example::

    python get_conjugation_rae.py amar

"""

from __future__ import annotations

import argparse
import json
from typing import Dict, Iterable, Tuple

import pyphen


REFLEXIVE_SUFFIXES = ["se", "me", "te", "nos", "os"]

ACCENTS = "áéíóú"
PLAIN = "aeiou"
ACCENT_MAP = dict(zip(PLAIN, ACCENTS))
ACCENT_REVERSE = str.maketrans(ACCENTS, PLAIN)
_dic = pyphen.Pyphen(lang="es")


def strip_reflexive(verb: str) -> Tuple[str, bool]:
    """Return verb without trailing reflexive pronoun and a flag."""
    for suf in REFLEXIVE_SUFFIXES:
        if verb.endswith(suf):
            return verb[: -len(suf)], True
    return verb, False


import cloudscraper
from bs4 import BeautifulSoup


class RAEConjugationFetcher:
    """Fetch and parse Spanish verb conjugations from the RAE website."""

    BASE_URL = "https://dle.rae.es"

    def __init__(self) -> None:
        self.scraper = cloudscraper.create_scraper(
            browser={"browser": "firefox", "platform": "windows", "desktop": True},
            delay=1.0,  # polite throttle
        )

    def fetch_html(self, verb: str) -> str:
        """Return the HTML for the RAE page of ``verb``."""
        resp = self.scraper.get(f"{self.BASE_URL}/{verb}", timeout=10)
        resp.raise_for_status()
        return resp.text

    def _parse_non_personal(self, table: BeautifulSoup) -> Dict[str, str]:
        """Parse tables without pronouns (infinitive, gerund, participle)."""
        data: Dict[str, str] = {}
        rows = list(table.find_all("tr"))
        it = iter(rows)
        for row in it:
            headings = [c.get_text("", strip=True) for c in row.find_all("th")]
            if not headings:
                continue
            next_row = next(it, None)
            if not next_row:
                break
            values = [c.get_text("", strip=True) for c in next_row.find_all("td")]
            for h, v in zip(headings, values):
                data[h] = v
        return data

    def _parse_personal(self, table: BeautifulSoup) -> Dict[str, Dict[str, str]]:
        """Parse tables that contain pronoun based conjugations."""
        rows = table.find_all("tr")
        headers = [c.get_text("", strip=True) for c in rows[0].find_all(["th", "td"])]
        tenses = headers[3:]
        result: Dict[str, Dict[str, str]] = {t: {} for t in tenses}

        for row in rows[1:]:
            cells = [c.get_text("", strip=True) for c in row.find_all(["th", "td"])]
            if len(cells) == len(tenses) + 3:
                _, _, pronoun = cells[:3]
                forms = cells[3:]
            elif len(cells) == len(tenses) + 2:
                _, pronoun = cells[:2]
                forms = cells[2:]
            elif len(cells) == len(tenses) + 1:
                pronoun = cells[0]
                forms = cells[1:]
            else:
                continue
            for tense, form in zip(tenses, forms):
                result.setdefault(tense, {})[pronoun] = form
        return result

    def _parse_conjugation(self, html: str) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Return a nested dict containing all conjugations found in ``html``."""
        soup = BeautifulSoup(html, "html.parser")
        section = soup.find(id=lambda x: x and x.startswith("conjugacion"))
        if not section:
            return {}

        conjugations: Dict[str, Dict[str, Dict[str, str]]] = {}
        for block in section.find_all("div", class_="c-collapse"):
            title_elem = block.find("h3")
            mood = (
                title_elem.get_text(" ", strip=True)
                if title_elem
                else block.get("id", "")
            )
            for table in block.find_all("table"):
                first_row = table.find("tr")
                if first_row and len(first_row.find_all("th")) <= 2:
                    # Non-personal forms: infinitive, participle, ...
                    data = self._parse_non_personal(table)
                    conjugations.setdefault(mood, {}).update(
                        {k: {"": v} for k, v in data.items()}
                    )
                else:
                    data = self._parse_personal(table)
                    conjugations.setdefault(mood, {}).update(data)
        return conjugations

    def get_conjugation(self, verb: str) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Fetch and parse the RAE conjugation table for ``verb``."""
        html = self.fetch_html(verb)
        return self._parse_conjugation(html)


class RAEConjugationTransformer:
    """Convert raw RAE tables into the project's conjugation format."""

    def __init__(self, verb: str, is_reflexive: bool = False) -> None:
        self.verb = verb
        self.is_reflexive = is_reflexive

    PERSON_MAP = {
        "yo": "1st_singular",
        "tú": "2nd_singular",
        "tú / vos": "2nd_singular",
        "vos": "2nd_singular",
        "usted": "3rd_singular",
        "él, ella": "3rd_singular",
        "nosotros, nosotras": "1st_plural",
        "vosotros, vosotras": "2nd_plural",
        "ustedes": "3rd_plural",
        "ellos, ellas": "3rd_plural",
    }

    INDICATIVE_MAP = {
        "Presente": "indicativo_presente",
        "Pretérito perfecto simple / Pretérito": "indicativo_preterito",
        "Pretérito imperfecto / Copretérito": "indicativo_imperfecto",
        "Futuro simple / Futuro": "indicativo_futuro",
        "Condicional simple / Pospretérito": "condicional",
    }

    SUBJUNCTIVE_MAP = {
        "Presente": "subjuntivo_presente",
        "Pretérito imperfecto / Pretérito": "subjuntivo_imperfecto",
        "Futuro simple / Futuro": "subjuntivo_futuro",
    }

    def _clean(self, text: str) -> str:
        for sep in [" / ", " o ", " u "]:
            if sep in text:
                text = text.split(sep)[0]
        return text.strip()

    def _syllables(self, word: str) -> list[str]:
        return _dic.inserted(word).split("-")

    def _stress_index(self, word: str) -> int:
        syls = self._syllables(word)
        for i, s in enumerate(syls):
            if any(c in ACCENTS for c in s):
                return i
        if word[-1].lower() in ("n", "s") or word[-1].lower() in PLAIN:
            return max(len(syls) - 2, 0)
        return len(syls) - 1

    def _apply_accent(self, word: str, index: int) -> str:
        syls = self._syllables(word)
        if index < 0 or index >= len(syls):
            return word
        s = syls[index]
        if any(c in ACCENTS for c in s):
            syls[index] = s
        else:
            pos = -1
            for j in range(len(s) - 1, -1, -1):
                ch = s[j].lower()
                if ch in "aeo":
                    pos = j
                    break
            if pos == -1:
                for j in range(len(s) - 1, -1, -1):
                    if s[j].lower() in "iu":
                        pos = j
                        break
            if pos != -1:
                ch = s[pos]
                accent = ACCENT_MAP.get(ch.lower(), ch)
                s = s[:pos] + accent + s[pos + 1 :]
            syls[index] = s
        return "".join(syls)

    def _map_personal(self, mapping: Dict[str, str]) -> Dict[str, str]:
        result: Dict[str, str] = {}
        for pronoun, value in mapping.items():
            key = pronoun.split("/")[0].split(",")[0].strip().lower()
            person = self.PERSON_MAP.get(pronoun) or self.PERSON_MAP.get(key)
            if person:
                result[person] = self._clean(value)
        return result

    def _add_reflexive(self, out: Dict[str, dict | str]) -> None:
        pronouns = {
            "1st_singular": "me",
            "2nd_singular": "te",
            "3rd_singular": "se",
            "1st_plural": "nos",
            "2nd_plural": "os",
            "3rd_plural": "se",
        }

        base = self.verb
        if base.endswith("se"):
            base = base[:-2]
        ending = base[-2:]

        def attach_affirmative(form: str, pron: str) -> str:
            original = form
            if pron == "nos" and form.endswith("mos"):
                form = form[:-1]
                result = form + pron
            elif pron == "os" and form.endswith("d"):
                trimmed = form[:-1]
                if base == "ir" and original == "id":
                    return "idos"
                if ending == "ir" and trimmed.endswith("i"):
                    trimmed = trimmed[:-1] + "í"
                result = trimmed + pron
                return result
            else:
                result = form + pron

            if any(c in ACCENTS for c in original):
                return result

            orig_idx = self._stress_index(original)
            new_default = self._stress_index(result.translate(ACCENT_REVERSE))
            if orig_idx != new_default:
                result = self._apply_accent(result, orig_idx)
            return result

        if "infinitivo" in out:
            out["infinitivo"] = f"{base}se"
        if "gerundio" in out:
            g = out["gerundio"]
            if g.endswith("ando"):
                g = g[:-4] + "ándose"
            elif g.endswith("iendo"):
                g = g[:-5] + "iéndose"
            elif g.endswith("yendo"):
                g = g[:-5] + "yéndose"
            else:
                g = g + "se"
            out["gerundio"] = g
        if "participio" in out:
            out["participio"] = ""

        for key, mapping in out.items():
            if not isinstance(mapping, dict):
                continue
            for person, pron in pronouns.items():
                if person not in mapping:
                    continue
                form = mapping[person]
                if key == "imperativo_affirmativo":
                    mapping[person] = attach_affirmative(form, pron)
                elif key == "imperativo_negativo":
                    if form.startswith("no "):
                        form = form[3:]
                    mapping[person] = f"no {pron} {form}"
                else:
                    mapping[person] = f"{pron} {form}"

    def transform(
        self, data: Dict[str, Dict[str, Dict[str, str]]]
    ) -> Dict[str, dict | str]:
        out: Dict[str, dict | str] = {}

        non_personal = data.get("Formas no personales", {})
        for src, dst in {
            "Infinitivo": "infinitivo",
            "Gerundio": "gerundio",
            "Participio": "participio",
        }.items():
            if src in non_personal:
                out[dst] = self._clean(non_personal[src].get("", ""))

        indicativo = data.get("Indicativo", {})
        for src, dst in self.INDICATIVE_MAP.items():
            if src in indicativo:
                out[dst] = self._map_personal(indicativo[src])

        subjuntivo = data.get("Subjuntivo", {})
        for src, dst in self.SUBJUNCTIVE_MAP.items():
            if src in subjuntivo:
                out[dst] = self._map_personal(subjuntivo[src])

        imperativo = data.get("Imperativo", {})
        if "Imperativo" in imperativo:
            out["imperativo_affirmativo"] = self._map_personal(imperativo["Imperativo"])
            if "1st_plural" not in out["imperativo_affirmativo"]:
                subj = out.get("subjuntivo_presente")
                if isinstance(subj, dict) and "1st_plural" in subj:
                    out["imperativo_affirmativo"]["1st_plural"] = subj["1st_plural"]

        subj_pres = out.get("subjuntivo_presente")
        if subj_pres:
            neg: Dict[str, str] = {}
            for person in [
                "2nd_singular",
                "3rd_singular",
                "1st_plural",
                "2nd_plural",
                "3rd_plural",
            ]:
                if person in subj_pres:
                    neg[person] = f"no {subj_pres[person]}"
            if neg:
                out["imperativo_negativo"] = neg

        raw_inf = data.get("Formas no personales", {}).get("Infinitivo", {}).get("", "")
        raw_is_reflexive = raw_inf.strip().endswith("se")

        if self.is_reflexive and not raw_is_reflexive:
            self._add_reflexive(out)

        return out


def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Scrape conjugations from RAE")
    parser.add_argument("verb", help="Spanish verb to fetch")
    args = parser.parse_args(argv)

    fetcher = RAEConjugationFetcher()
    base, is_reflexive = strip_reflexive(args.verb)
    raw = fetcher.get_conjugation(base)
    transformer = RAEConjugationTransformer(args.verb, is_reflexive=is_reflexive)
    conjugations = transformer.transform(raw)
    print(json.dumps(conjugations, ensure_ascii=False, indent=2))


if __name__ == "__main__":  # pragma: no cover - simple CLI
    main()
