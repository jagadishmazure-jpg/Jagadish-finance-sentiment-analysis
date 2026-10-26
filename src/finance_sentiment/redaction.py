"""PII redaction for free-text financial documents.

Checklist (every item has a test in tests/test_redaction.py):
- CARD NUMBERS: 13-19 digits, optionally grouped with spaces or dashes.
- EMAIL ADDRESSES.
- Phone numbers (international-style digit groups).
- US-style Social Security Numbers (ddd-dd-dddd).

Redaction replaces the matched value with a typed placeholder so a
reviewer can see *that* something was removed and *what kind* of thing
it was, without seeing the value. This module never logs the original.
"""

import re
from dataclasses import dataclass, field

_CARD = re.compile(r"\b(?:\d[ -]?){12,18}\d\b")
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_PHONE = re.compile(r"\+?\d[\d\s().-]{7,}\d")


@dataclass
class RedactionResult:
    text: str
    found: list = field(default_factory=list)

    def __post_init__(self):
        # Deduplicate while preserving order.
        seen = set()
        unique = []
        for item in self.found:
            if item not in seen:
                seen.add(item)
                unique.append(item)
        self.found = unique


def redact(text):
    found = []

    # Order matters: card numbers first (they look like phone numbers),
    # then SSN, then email, then phone.
    text_holder = [text]
    text_holder[0] = _CARD.sub(lambda m: (found.append("card_number"), "[CARD REDACTED]")[1], text_holder[0])
    text_holder[0] = _SSN.sub(lambda m: (found.append("ssn"), "[SSN REDACTED]")[1], text_holder[0])
    text_holder[0] = _EMAIL.sub(lambda m: (found.append("email"), "[EMAIL REDACTED]")[1], text_holder[0])
    # Phone last, and only digit runs that still look like a phone
    # number (7+ digits with separators); card/SSN are already gone.
    text_holder[0] = _PHONE.sub(lambda m: (found.append("phone"), "[PHONE REDACTED]")[1], text_holder[0])
    return RedactionResult(text=text_holder[0], found=found)
