"""Brand / name check with a hashed blocklist.

The blocklist is stored as SHA-256 hashes of normalised names, never
as plain names, so this file itself does not repeat the names it
guards against. The checker normalises candidate text (lowercase,
non-alphanumerics to spaces), builds every 1- to 4-word n-gram, hashes
each, and reports any hash in the blocklist.

The test in tests/test_brand.py asserts the blocklist is non-empty;
an empty blocklist would check nothing, which is a failure mode that
has bitten this portfolio before.
"""

import hashlib
import re

# SHA-256 digests of normalised blocked names, stored as hashes only
# (the plain names are never written in this repo). Non-empty by
# construction; see tests/test_brand.py::test_brand_blocklist_is_non_empty.
BLOCKED_HASHES = frozenset({
    "c952a08fdb0ff916b78a489ff321a4eb73d258612ededdd834c5a7c55fbc6c70",
    "17e9b17189f2f67e00b4c8dce8a6bedb38051ee221602fd52c88650ef9f68687",
    "5e43fa8fc186bf403a2de960d645a0cfc4bd2cf3fe59121bac118b48b9e00b89",
})

_TOKEN = re.compile(r"[a-z0-9]+")


def _hash(phrase):
    return hashlib.sha256(phrase.encode("utf-8")).hexdigest()


def check_text(text):
    """Return the list of blocked-phrase hashes found in ``text``."""
    tokens = _TOKEN.findall(text.lower())
    found = []
    for n in range(1, 5):
        for i in range(len(tokens) - n + 1):
            phrase = " ".join(tokens[i:i + n])
            digest = _hash(phrase)
            if digest in BLOCKED_HASHES and digest not in found:
                found.append(digest)
    return found
