# English causal reader position · 2026-11-09

Scope: fix initial reading position and disclosure visibility only. The user paused Chinese deployment; private repository/settings remain unchanged. No split, font, color, card-shape or course-content changes, and no commit/push.

Reproduction at1440×1000: U2 first card was obscured by47.78px of the sticky bottom navigation; reader sync explicitly reset first-step scrollTop to0. Styling and mirrored markup could settle after that calculation.

The reader now calculates the usable area between actual sticky tabs and bottom controls. New collapsed opening steps start from the top and scroll only enough to show their card and connector. Opened cards preserve a readable heading and a capped preview of their explanation. Existing readable positions remain unchanged. Previous/next and keyboard disclosure remain native controls. A guarded following-frame pass and stylesheet-load alignment handle delayed layout without acting on detached or superseded selections. Runtime cache versions updated together.

Tests: six regression cases first failed, then passed (initial bottom overlap, expansion, no unnecessary movement, above-tab selection, oversized headings, oversized explanation previews). Full suite:101Node tests,25Python tests;37English scripts parsed; strict canonical parity101chains/382steps,9Unit APIs,240study cards unchanged.

Browser: U2–U9 initial cards sit fully below tabs and above bottom controls. At1440px, normal connector clearance is approximately42px (U9’s wrapped connector approximately48px). Initial U2 scroll is90px, preserving more header than a blanket jump. U2 expansion exposes164px of explanation before the bottom controls. Previous/next and Enter toggling verified. At390px, no horizontal overflow (372px reading width/scrollWidth) and no selected-row occlusion;1280px desktop also checked. Temporary viewport reset.

Preview: http://127.0.0.1:8181/english-site/?lang=en&v=reading-position-fixed
