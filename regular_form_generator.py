from get_conjugation_rae import RAEConjugationTransformer


class RegularFormGenerator:
    """Generate hypothetical regular Spanish verb forms."""

    FORM_ID_TO_NAME = {
        0: "infinitivo",
        1: "gerundio",
        2: "participio",
        3: "indicativo_presente",
        4: "indicativo_preterito",
        5: "indicativo_imperfecto",
        6: "indicativo_futuro",
        7: "condicional",
        8: "subjuntivo_presente",
        9: "subjuntivo_imperfecto",
        10: "subjuntivo_futuro",
        11: "imperativo_affirmativo",
        12: "imperativo_negativo",
    }

    PERSON_ID_TO_NAME = {
        0: "not_applicable",
        11: "1st_singular",
        21: "2nd_singular",
        31: "3rd_singular",
        12: "1st_plural",
        22: "2nd_plural",
        32: "3rd_plural",
    }

    FORM_NAME_TO_ID = {v: k for k, v in FORM_ID_TO_NAME.items()}
    PERSON_NAME_TO_ID = {v: k for k, v in PERSON_ID_TO_NAME.items()}

    def get_verb_stem_and_ending(self, verb):
        """Extract stem and ending from a verb.

        Returns tuple (stem, ending, is_reflexive).
        """
        if verb.endswith("se"):
            base_verb = verb[:-2]
            if base_verb.endswith("ar"):
                return base_verb[:-2], "ar", True
            elif base_verb.endswith("er"):
                return base_verb[:-2], "er", True
            elif base_verb.endswith("ir") or base_verb.endswith("ír"):
                return base_verb[:-2], "ir", True
            else:
                return base_verb, "", True

        if verb.endswith("ar"):
            return verb[:-2], "ar", False
        elif verb.endswith("er"):
            return verb[:-2], "er", False
        elif verb.endswith("ir") or verb.endswith("ír"):
            return verb[:-2], "ir", False
        else:
            return verb, "", False

    def get_reflexive_pronoun(self, person):
        pronouns = {
            "1st_singular": "me",
            "2nd_singular": "te",
            "3rd_singular": "se",
            "1st_plural": "nos",
            "2nd_plural": "os",
            "3rd_plural": "se",
        }
        return pronouns.get(person, "")

    def generate(self, verb, form, person):
        """Generate the regular conjugation for the given verb, form and person."""
        stem, ending, is_reflexive = self.get_verb_stem_and_ending(verb)

        if isinstance(form, int):
            form = self.FORM_ID_TO_NAME.get(form, form)
        if isinstance(person, int):
            person = self.PERSON_ID_TO_NAME.get(person, person)

        if form == "infinitivo":
            return verb
        elif form == "gerundio":
            base_form = stem + ("ando" if ending == "ar" else "iendo")
            if is_reflexive:
                if base_form.endswith("ando"):
                    return base_form.replace("ando", "ándose")
                elif base_form.endswith("iendo"):
                    return base_form.replace("iendo", "iéndose")
                elif base_form.endswith("yendo"):
                    return base_form.replace("yendo", "yéndose")
                return base_form + "se"
            return base_form
        elif form == "participio":
            if is_reflexive:
                return ""
            if ending == "ar":
                return stem + "ado"
            else:
                return stem + "ido"

        if person == "not_applicable":
            return ""

        conjugations = {
            "indicativo_presente": {
                "ar": {
                    "1st_singular": "o",
                    "2nd_singular": "as",
                    "3rd_singular": "a",
                    "1st_plural": "amos",
                    "2nd_plural": "áis",
                    "3rd_plural": "an",
                },
                "er": {
                    "1st_singular": "o",
                    "2nd_singular": "es",
                    "3rd_singular": "e",
                    "1st_plural": "emos",
                    "2nd_plural": "éis",
                    "3rd_plural": "en",
                },
                "ir": {
                    "1st_singular": "o",
                    "2nd_singular": "es",
                    "3rd_singular": "e",
                    "1st_plural": "imos",
                    "2nd_plural": "ís",
                    "3rd_plural": "en",
                },
            },
            "indicativo_preterito": {
                "ar": {
                    "1st_singular": "é",
                    "2nd_singular": "aste",
                    "3rd_singular": "ó",
                    "1st_plural": "amos",
                    "2nd_plural": "asteis",
                    "3rd_plural": "aron",
                },
                "er": {
                    "1st_singular": "í",
                    "2nd_singular": "iste",
                    "3rd_singular": "ió",
                    "1st_plural": "imos",
                    "2nd_plural": "isteis",
                    "3rd_plural": "ieron",
                },
                "ir": {
                    "1st_singular": "í",
                    "2nd_singular": "iste",
                    "3rd_singular": "ió",
                    "1st_plural": "imos",
                    "2nd_plural": "isteis",
                    "3rd_plural": "ieron",
                },
            },
            "indicativo_imperfecto": {
                "ar": {
                    "1st_singular": "aba",
                    "2nd_singular": "abas",
                    "3rd_singular": "aba",
                    "1st_plural": "ábamos",
                    "2nd_plural": "abais",
                    "3rd_plural": "aban",
                },
                "er": {
                    "1st_singular": "ía",
                    "2nd_singular": "ías",
                    "3rd_singular": "ía",
                    "1st_plural": "íamos",
                    "2nd_plural": "íais",
                    "3rd_plural": "ían",
                },
                "ir": {
                    "1st_singular": "ía",
                    "2nd_singular": "ías",
                    "3rd_singular": "ía",
                    "1st_plural": "íamos",
                    "2nd_plural": "íais",
                    "3rd_plural": "ían",
                },
            },
            "condicional": {
                "ar": {
                    "1st_singular": "aría",
                    "2nd_singular": "arías",
                    "3rd_singular": "aría",
                    "1st_plural": "aríamos",
                    "2nd_plural": "aríais",
                    "3rd_plural": "arían",
                },
                "er": {
                    "1st_singular": "ería",
                    "2nd_singular": "erías",
                    "3rd_singular": "ería",
                    "1st_plural": "eríamos",
                    "2nd_plural": "eríais",
                    "3rd_plural": "erían",
                },
                "ir": {
                    "1st_singular": "iría",
                    "2nd_singular": "irías",
                    "3rd_singular": "iría",
                    "1st_plural": "iríamos",
                    "2nd_plural": "iríais",
                    "3rd_plural": "irían",
                },
            },
            "subjuntivo_presente": {
                "ar": {
                    "1st_singular": "e",
                    "2nd_singular": "es",
                    "3rd_singular": "e",
                    "1st_plural": "emos",
                    "2nd_plural": "éis",
                    "3rd_plural": "en",
                },
                "er": {
                    "1st_singular": "a",
                    "2nd_singular": "as",
                    "3rd_singular": "a",
                    "1st_plural": "amos",
                    "2nd_plural": "áis",
                    "3rd_plural": "an",
                },
                "ir": {
                    "1st_singular": "a",
                    "2nd_singular": "as",
                    "3rd_singular": "a",
                    "1st_plural": "amos",
                    "2nd_plural": "áis",
                    "3rd_plural": "an",
                },
            },
            "subjuntivo_imperfecto": {
                "ar": {
                    "1st_singular": "ara",
                    "2nd_singular": "aras",
                    "3rd_singular": "ara",
                    "1st_plural": "áramos",
                    "2nd_plural": "arais",
                    "3rd_plural": "aran",
                },
                "er": {
                    "1st_singular": "iera",
                    "2nd_singular": "ieras",
                    "3rd_singular": "iera",
                    "1st_plural": "iéramos",
                    "2nd_plural": "ierais",
                    "3rd_plural": "ieran",
                },
                "ir": {
                    "1st_singular": "iera",
                    "2nd_singular": "ieras",
                    "3rd_singular": "iera",
                    "1st_plural": "iéramos",
                    "2nd_plural": "ierais",
                    "3rd_plural": "ieran",
                },
            },
            "subjuntivo_futuro": {
                "ar": {
                    "1st_singular": "are",
                    "2nd_singular": "ares",
                    "3rd_singular": "are",
                    "1st_plural": "áremos",
                    "2nd_plural": "areis",
                    "3rd_plural": "aren",
                },
                "er": {
                    "1st_singular": "iere",
                    "2nd_singular": "ieres",
                    "3rd_singular": "iere",
                    "1st_plural": "iéremos",
                    "2nd_plural": "iereis",
                    "3rd_plural": "ieren",
                },
                "ir": {
                    "1st_singular": "iere",
                    "2nd_singular": "ieres",
                    "3rd_singular": "iere",
                    "1st_plural": "iéremos",
                    "2nd_plural": "iereis",
                    "3rd_plural": "ieren",
                },
            },
            "imperativo_affirmativo": {
                "ar": {
                    "2nd_singular": "a",
                    "3rd_singular": "e",
                    "1st_plural": "emos",
                    "2nd_plural": "ad",
                    "3rd_plural": "en",
                },
                "er": {
                    "2nd_singular": "e",
                    "3rd_singular": "a",
                    "1st_plural": "amos",
                    "2nd_plural": "ed",
                    "3rd_plural": "an",
                },
                "ir": {
                    "2nd_singular": "e",
                    "3rd_singular": "a",
                    "1st_plural": "amos",
                    "2nd_plural": "id",
                    "3rd_plural": "an",
                },
            },
            "imperativo_negativo": {
                "ar": {
                    "2nd_singular": "es",
                    "3rd_singular": "e",
                    "1st_plural": "emos",
                    "2nd_plural": "éis",
                    "3rd_plural": "en",
                },
                "er": {
                    "2nd_singular": "as",
                    "3rd_singular": "a",
                    "1st_plural": "amos",
                    "2nd_plural": "áis",
                    "3rd_plural": "an",
                },
                "ir": {
                    "2nd_singular": "as",
                    "3rd_singular": "a",
                    "1st_plural": "amos",
                    "2nd_plural": "áis",
                    "3rd_plural": "an",
                },
            },
        }

        if form in ["indicativo_futuro", "condicional"]:
            base_verb = verb[:-2] if is_reflexive else verb
            if form == "indicativo_futuro":
                endings = {
                    "1st_singular": "é",
                    "2nd_singular": "ás",
                    "3rd_singular": "á",
                    "1st_plural": "emos",
                    "2nd_plural": "éis",
                    "3rd_plural": "án",
                }
            else:
                endings = {
                    "1st_singular": "ía",
                    "2nd_singular": "ías",
                    "3rd_singular": "ía",
                    "1st_plural": "íamos",
                    "2nd_plural": "íais",
                    "3rd_plural": "ían",
                }
            if person in endings:
                conjugated = base_verb + endings[person]
                if is_reflexive:
                    pronoun = self.get_reflexive_pronoun(person)
                    return f"{pronoun} {conjugated}"
                return conjugated

        if form in conjugations and ending in conjugations[form]:
            if person in conjugations[form][ending]:
                base_conjugation = stem + conjugations[form][ending][person]
                if is_reflexive:
                    pronoun = self.get_reflexive_pronoun(person)
                    if form == "imperativo_affirmativo":
                        if person == "2nd_plural" and base_conjugation.endswith("d"):
                            trimmed = base_conjugation[:-1]
                            if verb.rstrip("se") == "ir":
                                return "idos"
                            if ending == "ir" and trimmed.endswith("i"):
                                trimmed = trimmed[:-1] + "í"
                            base_form = trimmed
                        else:
                            base_form = base_conjugation
                        return RAEConjugationTransformer(verb)._attach_affirmative(
                            base_form,
                            pronoun,
                            verb.rstrip("se"),
                            ending,
                        )
                    result = f"{pronoun} {base_conjugation}"
                    if form == "imperativo_negativo":
                        return f"no {result}"
                    return result
                else:
                    if form == "imperativo_negativo":
                        return f"no {base_conjugation}"
                    return base_conjugation
        return ""
