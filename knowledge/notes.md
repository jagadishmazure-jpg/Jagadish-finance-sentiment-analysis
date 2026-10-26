# Knowledge notes (distilled, in the author's own words)

Source material consulted: a brochure for a multi-week finance AI
programme. No sentences from it are reproduced here, and no
affiliation with any programme or institution is claimed. The
patterns below are the author's paraphrase of the use cases it
describes.

## Patterns distilled

1. **Tone in leadership commentary as a research input.** Read
   what executives say on calls and what filings disclose, and
   turn shifts in tone, confidence, and forward-looking language
   into signals that sit alongside numbers in research and credit
   work. This repo implements that pattern, and only that pattern,
   on synthetic text.
2. **Ask whether a number deserves action.** A sentiment figure
   without a reliability check invites over-trust. The useful
   question is not what the score is, but what would have to be
   true for it to be acted on: enough supporting language, a
   clear direction, and a human in the loop when any of those are
   missing. That question is the whole reason for the gate here.
3. **Judge the judge.** When a model rates text, its ratings need
   their own evaluation: run comparisons in both orders, keep ties
   out of the rate denominators, check agreement against human
   labels, and report uncertainty as an interval. A single
   accuracy figure on a small set is not an evaluation.
4. **Precision and recall are a trade-off to choose, not a score
   to maximise.** Missing a real signal and raising a false one
   cost different things in different workflows; report both, per
   label, with counts, and let the workflow owner choose the
   operating point. The gate's threshold is that choice, made
   explicit.
5. **PII risk travels with financial text.** Documents that carry
   financial discussion can also carry personal identifiers. Any
   pipeline that reads them needs redaction before scoring and
   before anything is logged or shown to a reviewer.
6. **Neighbouring patterns, not built here.** The same source
   material describes invoice reimbursement automation, credit
   memo underwriting with borrower data, compliance screening
   workflows, portfolio risk monitoring agents, and a multi-agent
   "bank" orchestration. Those are separate repos in this series
   (see `docs/related-repos.md`); this repo does not duplicate
   them, and it never uses real loan or customer data — every
   pattern here is exercised on synthetic text only.

## What was deliberately not taken from the source

- No programme structure, pricing, faculty, mentor, or enrolment
  detail: irrelevant to the code and not this repo's to repeat.
- No claim about real datasets: where the source describes work
  on real records, this repo substitutes synthetic data and says
  so everywhere, because a portfolio demo must not imply access
  to data it does not have.
