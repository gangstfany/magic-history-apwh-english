# English edition verification · 2026-11-07

Built against the exact Chinese source revision recorded in ENGLISH-EDITION.json. 4,137 display strings have translations; 101 chains and 382 steps preserve their canonical structures; all nine Unit APIs and 240 study-card IDs remain identical. 95 refined/U2 chains are in the visual reader, with U1 retaining its confirmed comparison UI. All 234 image hashes remain unchanged.

Checks: 89 baseline Node tests; 8 baseline Python tests; 11 English parsing/coverage tests; 18 homepage tests; 37 built English scripts parsed; an independent HTML scan confirms no Chinese display text and identical element/tag order and IDs. No account pin, Chinese course source, artwork image or course factual coverage was changed.

Browser: switching Chinese U3 step 3 to English and back retains the same Unit/step; U1 gender theme/group/case keys carry across languages; APWH U4 Potosi study-point ID and expanded state are retained through both directions; quiz prompt/options/feedback render in English; the EN account dialog uses English display copy without changing authentication logic. At 390px, outer document width/scrollWidth both 390 and course width/scrollWidth both 372. Visible English DOM snapshot contains no Chinese outside the intentional Chinese language-switch label. Temporary viewport restored.

Local display aliases retain original source names in catalog source keys. Conflicting stylistic translations were reviewed; no substantive source/URL/HTML changes were needed. Greater-than signs in historical hierarchy prose are independently verified and safely escaped.

The local verified preview uses an allowlisted generated snapshot under /private/tmp to avoid local synchronization-created duplicate files in the Documents build directory. CI defaults to _site on Linux and rejects incomplete translations. No publish action performed.

## English reading-space adjustment

English edition only: wider reading columns (44%, bounded to 480–620 px), labels above paired comparison controls, shorter navigation labels and helper copy, more padding and line spacing for event cards and paragraphs, and more compact image-card framing. Full historical explanations and evidence remain. Chinese source unchanged.

Verified strict English build, parity for 101 chains / 382 steps and 240 cards, independent HTML scan, desktop U1 and expanded U2 interaction, and 390 px viewport without horizontal overflow (outer 390/390; course 372/372). Temporary viewport reset. Preview: http://127.0.0.1:8181/english-site/?lang=en&v=reading-space-20261107 . No commit or push.

## Approved typography applied to all units

Supersedes wider-column experiment: original 34% (380–430 px) reading column, original selector rows and map popup positions restored. U1 approved prototype typography/scan titles ported; full titles and evidence retained on expansion. U1 comparison rails and U2–U9 causal connector labels use 12 px type and minimum 30 px height, with 15 px arrows. Multi-line connectors may grow to avoid clipping (U9 first connector is 36 px at tested width). Browser checked U1–U9 main-chain connectors: U1–U8 30 px, U9 36 px wrapped; all 12 px. Strict English verification passed: 101 chains, 382 steps, 240 study cards; no untranslated display text; main HTML structure/IDs unchanged. Main EN preview and standalone prototype updated. No commit/push.

## Review fixes after 19b6050

Corrected the inherited Timbuktu event to describe Islam spreading into West Africa through trans-Saharan connections (AMSCO PDF194 / printed130), and restored “Most scholars believe” to both Sundiata displays (PDF110 / printed46; PDF170 / printed106). Source translation keys and canonical IDs retained.

English chain-row labels now use Main / Extra inside the original42px label column. Desktop control x-coordinates match (893.37px); mobile390px coordinates match (71px), without horizontal overflow. No split/layout/color changes.

Exit practice restores filters and renders the practice menu. Internal module transitions skip reopening it. Regression tests initially reproduced missing menu and both content defects; all four now pass. Browser confirmed U2 preserved and Practice selected with the quiz entry displayed after exit; active-quiz transitions to Map and Causal chains also work.

Validation:93 Node tests,19 Python tests,37 built scripts parsed, strict English coverage/canonical parity and full240-card content verification passed. No commit or push for this follow-up.
