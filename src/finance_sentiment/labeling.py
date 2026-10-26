"""Hand-labeled SYNTHETIC ground-truth set.

Every transcript and filing excerpt below was invented for this repo.
Company names are invented ("Acme Widgets", "Harborline Foods",
"Northgate Tools", "Ficton Retail"); tickers are invented
(ACMW, HBRF, NGTG, FCTN). No real company, filing, or call is quoted.

12 items, 4 per label. This is a regression check set, not a quality
claim: with n=12, a single item moves accuracy by ~8 points, so the
demo reports counts alongside every rate (see metrics.wilson_ci).
"""

LABELED = [
    {
        "id": "call-01",
        "kind": "earnings_call",
        "company": "Acme Widgets",
        "text": "Revenue grew strongly, margins expanded, and demand remained robust. "
        "Management expressed confidence in the outlook for the year ahead.",
        "label": "positive",
    },
    {
        "id": "call-02",
        "kind": "earnings_call",
        "company": "Harborline Foods",
        "text": "Revenue declined, losses widened, and headwinds pressured margins. "
        "Management cited significant uncertainty about the next quarter.",
        "label": "negative",
    },
    {
        "id": "call-03",
        "kind": "earnings_call",
        "company": "Northgate Tools",
        "text": "Revenue was in line with the prior quarter. Management will host "
        "a follow-up call next week to discuss operations.",
        "label": "neutral",
    },
    {
        "id": "call-04",
        "kind": "earnings_call",
        "company": "Ficton Retail",
        "text": "Growth accelerated, the quarter beat expectations, and momentum "
        "remained healthy across every region we serve.",
        "label": "positive",
    },
    {
        "id": "call-05",
        "kind": "earnings_call",
        "company": "Acme Widgets",
        "text": "The quarter missed expectations, weakness persisted, and the "
        "downturn pressured results in every segment.",
        "label": "negative",
    },
    {
        "id": "call-06",
        "kind": "earnings_call",
        "company": "Harborline Foods",
        "text": "Results matched the prior quarter. The call covered scheduling, staffing, and "
        "the agenda for the next meeting.",
        "label": "neutral",
    },
    {
        "id": "filing-01",
        "kind": "filing_excerpt",
        "company": "Northgate Tools",
        "text": "Profit improved, gains were solid, and the business remained "
        "resilient despite a challenging operating environment.",
        "label": "positive",
    },
    {
        "id": "filing-02",
        "kind": "filing_excerpt",
        "company": "Ficton Retail",
        "text": "The filing notes a shortfall, contraction in orders, and "
        "deteriorating conditions that increased risk for the period.",
        "label": "negative",
    },
    {
        "id": "filing-03",
        "kind": "filing_excerpt",
        "company": "Acme Widgets",
        "text": "The excerpt lists reporting dates, document sections, and the "
        "location of the next scheduled disclosure.",
        "label": "neutral",
    },
    {
        "id": "filing-04",
        "kind": "filing_excerpt",
        "company": "Harborline Foods",
        "text": "Demand was robust, profit grew, and management described a "
        "record quarter with strong momentum into the next period.",
        "label": "positive",
    },
    {
        "id": "filing-05",
        "kind": "filing_excerpt",
        "company": "Northgate Tools",
        "text": "Losses widened, revenue declined sharply, and uncertainty "
        "remained high throughout the reporting period.",
        "label": "negative",
    },
    {
        "id": "filing-06",
        "kind": "filing_excerpt",
        "company": "Ficton Retail",
        "text": "The document describes filing procedures, page numbering, and "
        "the timetable for the next routine submission.",
        "label": "neutral",
    },
]


def labeled_pairs():
    """Return (texts, human_labels) in set order."""
    return [item["text"] for item in LABELED], [item["label"] for item in LABELED]
