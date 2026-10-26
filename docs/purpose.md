# Purpose and who it is for

This repo builds a small, fully auditable sentiment pipeline for
investment and credit research workflows, using invented data only.

It is for:

- **Analysts** who want a transparent baseline: every score can be
  recomputed by hand from the lexicon file.
- **Engineers** who want to see a reliability gate done properly:
  a score is not a decision, and weak scores must reach a human.
- **Evaluators** who want judge-evaluation hygiene in miniature:
  both presentation orders, ties kept out of denominators, agreement
  measured against human labels, and uncertainty reported as an
  interval rather than a bare percentage.

It is not for making real investment or credit decisions, and it
never touches real disclosures, real loan files, or real customer
data. All text here is synthetic. Any brochure pattern that inspired
this repo is distilled in the author's own words in `knowledge/`; no
source material is copied, and no affiliation with any programme or
institution is claimed.
