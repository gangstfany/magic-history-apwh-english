# APWH English mobile interaction review — 2026-11-09

Reviewed local build after b4c0bac. Local changes only; no commit/push.

## Confirmed issue and fix

At 320 × 568, open U1 Song Dynasty / Inca comparison on the map. The comparison card spans the small-screen map, but its z-index was 2 while map zoom controls used 3. The close button occupied x265–295 / y22–52; Zoom in overlapped its center. Clicking x280/y37 left the popup open and enabled Zoom out: the click zoomed the map instead of closing the comparison.

The existing <=1050px comparison layout now raises only the comparison popup to z-index 4. Its close button receives the click. No dimensions, text, colors, fonts, content, IDs, map bindings or image assets changed. Map controls become available again when the covering popup closes. Updated U1 integration asset cache version.

Browser regression: repeated the same coordinate click at 320 × 568 after rebuilding; popup closed and Zoom out remained disabled. Repeated closure successfully in the homepage iframe at 390 × 844.

## Other walkthroughs

- U1 full-image dialog: title, source/caption and Close available at 390px.
- U2 Next step: independent course page advances to step 2, updates map and image and exposes explanation; bottom navigation stays available within the reading panel.
- U9 supplementary selection: Public Health & Access opens its authored four steps.
- Trade library and Silk Roads: route, stop and preserved causal-origin controls present; mobile route/map captions wrap without global horizontal overflow.
- Practice at 320px: start, Back to practice and Back to map work; no answers submitted or stored practice results changed.
- Homepage 390px width equals scrollWidth (390). Standalone course 320px width equals scrollWidth (320).

An initial automated Next click in the nested homepage iframe failed because automation repositioned the outer page while scrolling the inner reading panel. The standalone page click succeeded. This was not treated as a confirmed website navigation defect.

Limits: browser viewport simulation, not a physical iOS/Android touch test; representative flows rather than every chain, image and route combination.

## Checks

- 102 Node tests; 14 source Python tests; 22 English Python tests: passed.
- Canonical parity: 101 chains / 382 steps unchanged; 240 cards and all 9 Unit APIs retained.
- No untranslated display strings; 37 built scripts parse; 234 images unchanged.
- git diff --check passed.
- Screenshot: workspace output/apwh-english-2026-11-07/mobile-comparison-fixed.png.
- Preview: http://127.0.0.1:8181/english-site/?lang=en
