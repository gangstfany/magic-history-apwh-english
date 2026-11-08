# APWH English legacy-event and practice review · 2026-11-08

First-pass reading of all 288 legacy map events; 101 entries revised with recorded local-source context and teacher clarification. The retained 187 entries were screened for obvious errors, not independently recertified line by line against the textbook. No online research or image downloads. No layout/CSS/font/color changes, no other-course edits, no commit or push.

| Unit / scope | Events screened | Revised |
|---|---:|---:|
| BACKGROUND-OR-DUPLICATE | 9 | 3 |
| U1 | 43 | 18 |
| U2 | 13 | 4 |
| U3 | 30 | 12 |
| U4 | 29 | 14 |
| U5 | 31 | 5 |
| U6 | 37 | 15 |
| U7 | 28 | 7 |
| U8 | 43 | 14 |
| U9 | 25 | 9 |

## Main changes

- Distinguish Benin at pin77 from Kongo at an existing west-central African regional anchor (pin91). Afonso is identified as a Kongo ruler; the modern Kinshasa point is explicitly not his court. No pins or source-event positions moved.
- Correct/qualify dates and causal claims: Single Whip silver taxation moved from U2 to U4 without changing sourceId5:6; Manila galleons1565–1815; Tordesillas1494; 1978CampDavidAccords versus1979peace treaty; 1979smallpoxcertification versus1980declaration; occupation/conquest stages distinguished.
- Separate complex processes: crops/population versus silver/inflation; imperial plans versus completed infrastructure; slave-trade abolition versus slavery abolition; worst-case voyage mortality versus AMSCO’s10–15% overall estimate; coerced labor and demographic losses rather than uniform regional outcomes.
- Remove unsupported absolute firsts, universal replacement narratives, ancient-hatred explanations and single-cause shortcuts. Religious, gender and political comparisons preserve differences among places and periods.
- Preserve quiz explanations after the first heading separator. Previously splitting every em/en dash silently converted10–15% and date ranges into separated numbers. Regression test reproduced the defect before the fix; browser confirmed10–15%nowrendersintact.
- Retain previous English quiz-review/progress keys for corrected events so copy/date corrections do not discard stored practice records. Canonical event IDs, source ordering, pins, study-card IDs and chain/image bindings retained.

## Sources and review

`src/apwh/legacy-event-revisions.json` records old text/date, revised text/date, sourceId, rationale, physical/printed AMSCO pages or existing reviewed local material, original source-body hash and old quiz key. It is teaching synthesis, not a claim of verbatim textbook quotation. Some textbook summaries themselves compress distinctions; teacher clarifications and existing corrected cards are identified separately. Exact citations were independently reviewed and tightened, including Westphalia, India planning, China1911, WWII, TRC, apartheid and global institutions.

The full local textbook extraction and existing user notes stayed in local output folders; no PDF/textbook content was added to a public runtime asset.

## Verification

95 Node tests and25 Python tests passed;37 built English scripts parsed. Strict English verification retains101chains/382steps,9UnitAPIs and240study-cardIDs; all240cardrelationsresolve. Public map still contains288eventsand113pins. All101revisionshaveoriginal-sourcehash/dateguards, so source drift fails before a correction can silently hit another event.

Browser verified Kongo search at pin91, U2 exclusion/U4 inclusion of revised silver taxation, and corrected Middle Passage prose in both search results and practice options. No answer submitted during final verification. Temporary viewport reset. Main EN preview and standalone prototype updated.

Preview: http://127.0.0.1:8181/english-site/?lang=en&v=legacy-review-20261108

Remaining lower-priority work from the earlier plan: published EN routing/deployment walkthrough; initial reading-scroll positioning; remaining English microcopy. This pass is not a guarantee that every retained historical assertion is error-free.
