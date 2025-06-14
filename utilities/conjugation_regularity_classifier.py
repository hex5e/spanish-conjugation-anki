from __future__ import annotations

import re

from .regular_form_generator import RegularFormGenerator

ACCENTS = "áéíóúÁÉÍÓÚ"
PLAIN = "aeiouAEIOU"
ACCENT_REVERSE = str.maketrans(ACCENTS + "üÜ", PLAIN + "uU")


class ConjugationRegularityClassifier:
    """Classify how a verb deviates from regular conjugation."""

    def __init__(self) -> None:
        self.generator = RegularFormGenerator()

    def _strip_accents(self, text: str) -> str:
        return text.translate(ACCENT_REVERSE)

    def _c_to_qu(self, regular: str) -> str:
        return re.sub(r"c([eéií])", r"qu\1", regular)

    def _g_to_gu(self, regular: str) -> str:
        return re.sub(r"g([eéií])", r"gu\1", regular)

    def _z_to_c(self, regular: str) -> str:
        return re.sub(r"z([eéií])", r"c\1", regular)

    def _g_to_j(self, regular: str) -> str:
        return re.sub(r"g([aoáó])", r"j\1", regular)

    def _gu_to_gue_dieresis(self, regular: str) -> str:
        return re.sub(r"gu([eéií])", r"gü\1", regular)

    def _guir_drop_u(self, regular: str) -> str:
        return re.sub(r"gu([aoáó])", r"g\1", regular)

    def _c_to_z_after_consonant(self, regular: str) -> str:
        return re.sub(r"(?<=[^aeiouáéíóúü])c([oaóá])", r"z\1", regular)

    def _i_to_y(self, regular: str) -> str:
        return re.sub(r"i([aeoáéó])", r"y\1", regular)

    def _accent_shift(self, regular: str) -> str:
        return regular  # accents handled separately

    def is_orthographic_variant(self, regular: str, actual: str) -> bool:
        # Check transformations in order
        candidates = [
            self._c_to_qu,
            self._g_to_gu,
            self._z_to_c,
            self._g_to_j,
            self._gu_to_gue_dieresis,
            self._guir_drop_u,
            self._c_to_z_after_consonant,
            self._i_to_y,
        ]
        for func in candidates:
            if func(regular) == actual:
                return True
        # Accent shift only
        if (
            self._strip_accents(regular) == self._strip_accents(actual)
            and regular != actual
        ):
            return True
        return False

    def classify(self, verb: str, conjugations: dict[str, dict[str, str]]) -> str:
        results = []
        for form, persons in conjugations.items():
            for person, actual in persons.items():
                regular = self.generator.generate(verb, form, person)
                if regular == actual:
                    continue
                if self.is_orthographic_variant(regular, actual):
                    results.append("orthographic")
                else:
                    results.append("morphological")
        if any(r == "morphological" for r in results):
            return "morphologically_irregular"
        if any(r == "orthographic" for r in results):
            return "orthographically_irregular"
        return "regular"
