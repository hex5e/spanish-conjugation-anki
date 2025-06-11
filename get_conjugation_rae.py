"""Fetch Spanish verb conjugations from the RAE dictionary website.

This script scrapes the conjugation tables from ``dle.rae.es``.  The
site sits behind Cloudflare so ``cloudscraper`` is used to emulate a
real browser.  Parsed results are printed as JSON to stdout.

Example::

    python get_conjugation_rae.py amar

"""

from __future__ import annotations

import argparse
import json
from typing import Dict, Iterable

import cloudscraper
from bs4 import BeautifulSoup

BASE = "https://dle.rae.es"


def _fetch_html(verb: str) -> str:
    """Return the HTML for the RAE page of ``verb``."""
    scraper = cloudscraper.create_scraper(
        browser={"browser": "firefox", "platform": "windows", "desktop": True},
        delay=1.0,  # polite throttle
    )
    resp = scraper.get(f"{BASE}/{verb}", timeout=10)
    resp.raise_for_status()
    return resp.text


def _parse_non_personal(table: BeautifulSoup) -> Dict[str, str]:
    """Parse tables without pronouns (infinitive, gerund, participle)."""
    data: Dict[str, str] = {}
    rows = list(table.find_all("tr"))
    it = iter(rows)
    for row in it:
        headings = [c.get_text(" ", strip=True) for c in row.find_all("th")]
        if not headings:
            continue
        next_row = next(it, None)
        if not next_row:
            break
        values = [c.get_text(" ", strip=True) for c in next_row.find_all("td")]
        for h, v in zip(headings, values):
            data[h] = v
    return data


def _parse_personal(table: BeautifulSoup) -> Dict[str, Dict[str, str]]:
    """Parse tables that contain pronoun based conjugations."""
    rows = table.find_all("tr")
    headers = [c.get_text(" ", strip=True) for c in rows[0].find_all(["th", "td"])]
    tenses = headers[3:]
    result: Dict[str, Dict[str, str]] = {t: {} for t in tenses}
    current_number = None
    current_person = None

    for row in rows[1:]:
        cells = [c.get_text(" ", strip=True) for c in row.find_all(["th", "td"])]
        if len(cells) == len(tenses) + 3:
            current_number, current_person, pronoun = cells[:3]
            forms = cells[3:]
        elif len(cells) == len(tenses) + 2:
            current_person, pronoun = cells[:2]
            forms = cells[2:]
        elif len(cells) == len(tenses) + 1:
            pronoun = cells[0]
            forms = cells[1:]
        else:
            continue
        for tense, form in zip(tenses, forms):
            result.setdefault(tense, {})[pronoun] = form
    return result


def _parse_conjugation(html: str) -> Dict[str, Dict[str, Dict[str, str]]]:
    """Return a nested dict containing all conjugations found in ``html``."""
    soup = BeautifulSoup(html, "html.parser")
    section = soup.find(id=lambda x: x and x.startswith("conjugacion"))
    if not section:
        return {}

    conjugations: Dict[str, Dict[str, Dict[str, str]]] = {}
    for block in section.find_all("div", class_="c-collapse"):
        title_elem = block.find("h3")
        mood = title_elem.get_text(" ", strip=True) if title_elem else block.get("id", "")
        for table in block.find_all("table"):
            first_row = table.find("tr")
            if first_row and len(first_row.find_all("th")) <= 2:
                # Non-personal forms: infinitive, participle, ...
                data = _parse_non_personal(table)
                conjugations.setdefault(mood, {}).update({k: {"": v} for k, v in data.items()})
            else:
                data = _parse_personal(table)
                conjugations.setdefault(mood, {}).update(data)
    return conjugations


def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Scrape conjugations from RAE")
    parser.add_argument("verb", help="Spanish verb to fetch")
    args = parser.parse_args(argv)

    html = _fetch_html(args.verb)
    conjugations = _parse_conjugation(html)
    print(json.dumps(conjugations, ensure_ascii=False, indent=2))


if __name__ == "__main__":  # pragma: no cover - simple CLI
    main()
