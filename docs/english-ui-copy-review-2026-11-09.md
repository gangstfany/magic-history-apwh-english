# English UI copy review — 2026-11-09

Scope: interface labels and hints only. Preserve historical prose, layout, styles, IDs, image bindings and the earlier reading-position fix. Local changes only; no commit or push.

Changes:
- Remove repeated Step/Stop nouns in counters, route return links and saved-step subtitles. Route locations use Stop; causal-reader locations use Step.
- Standardize Trade & exchange, Review list, Review mistakes, Theme and Case pair.
- Shorten selection, route-resume and practice-filter hints. Use Start quiz and Up to 10 questions; remove redundant items from practice statistics.
- Distinguish Back to practice during a quiz from Back to map on its landing page. The latter now actually switches to the map instead of reopening the practice menu.
- Update preview cache versions and the associated version assertion.

Verification:
- 102 Node tests, 14 source Python tests and 22 English-build Python tests passed.
- Strict English scan: 9 Unit APIs, 240 study cards, 95 visible chains, no untranslated display strings.
- Canonical parity: 101 chains / 382 steps unchanged; element order and IDs unchanged; 234 images unchanged. All 37 built scripts parsed.
- All 240 rendered cards and relation targets verified; git diff --check passed.
- Browser: U1 labels and short hint; U2 Trade & exchange, Stop counters and saved Step return; practice landing Start quiz and bounded count; Back to map preserves Unit 2; Back to practice restores Unit 2 and practice menu. No quiz answers submitted during this review.
- Review-list wording checked in source/build rather than manufacturing wrong answers in existing user progress.
- Screenshot: output/apwh-english-2026-11-07/ui-copy-practice.png (workspace root).

Preview: http://127.0.0.1:8181/english-site/?lang=en

This is a scoped UI-copy review, not a new historical-content audit. Chinese hosting and other repositories remain outside this batch.
