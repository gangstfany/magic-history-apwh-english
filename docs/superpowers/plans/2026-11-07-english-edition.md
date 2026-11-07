# APWH English Edition Implementation Plan

Goal: retain the Chinese edition’s complete layouts, IDs and learning content while serving English from the independent edition when EN is selected in the homepage.

Architecture: tracked Chinese baseline copied to an independent English checkout; audited English translation catalogs applied at build/runtime to canonical data and display strings. Homepage uses language-specific course URLs and a stable state handshake to preserve Unit/selection. No account changes, no unrelated course edits.

- [x] Inventory display content and store a source revision manifest.
- [x] Translate Units 1–9 chains, cards, quizzes, network and UI text.
- [x] Build English edition with no missing translations and verify ID/card/step/media parity.
- [x] Wire homepage language toggle and translate public homepage copy.
- [x] Verify Unit/event restoration, filters, favorites, language persistence and mobile geometry.
- [x] Deliver local preview for review before pushing new content.
