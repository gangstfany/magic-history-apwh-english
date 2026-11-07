# Magic History · AP World History — English Edition

Independent English edition: `gangstfany/magic-history-apwh-english`.

This edition preserves the Chinese course's layout, event and study-card IDs, historical coverage, map bindings, interaction templates, images and attribution. Display strings are translated faithfully through reviewed catalogs in `translations/`; baseline source stays traceable to the Chinese revision recorded in `ENGLISH-EDITION.json`.

## Build and verify

```sh
python3 scripts/build-site.py
node --test src/apwh/test-*.cjs tests/*.test.mjs src/workspace/*/*.test.cjs
python3 -m unittest discover -s src/apwh -p 'test_*.py'
python3 -m unittest discover -s scripts -p 'test_english*.py'
python3 scripts/build-english.py
python3 scripts/verify-english.py
node scripts/check-built-english.mjs
python3 -m http.server 8182 --bind 127.0.0.1 --directory _site
```

Publish only `_site/` after the strict English build succeeds. `--allow-incomplete` is for internal local review only and marks its output incomplete; verification rejects it. Never deploy an incomplete preview. The English workflow runs baseline checks first, then builds and validates English as its final artifact.

## Language routing

The homepage's Chinese/EN switch chooses the corresponding independent course URL. APWH retains the existing `module=apwh` message interface and canonical favorite IDs. Account code, release pins and other course repositories are not changed by this edition. The source-language archive is not a published learning entry point.

No textbook PDFs, private media or preview homepage copies belong in the public artifact. Source-image rights and historical qualifications remain intact; translation is not new historical authorship or an official scoring guarantee.
