# U3–U9 event images

Added 2026-11-01: 210 image assets mapped to all 327 steps across 89 U3–U9 chains. The existing U1 and U2 imagery is retained. These assets extend the existing left-map popup and image dialog; no layout or typography changes are required.

The collection includes event photographs, historical paintings/prints, original documents, production scenes, artifacts, and a small number of explanatory maps/data graphics. Adjacent stages may share a relevant source image. Historical representations and propaganda are identified in captions rather than treated as eyewitness evidence.

- `catalogue.json`: display title/date, representation limits, creator, source page, license, and per-step relevance.
- `event-image-sources.json`: public source metadata, original asset URL, transformation disclosure, and SHA-256 for each imported JPEG.
- `assets/events/`: local JPEGs; the page does not depend on third-party image hotlinks.

Sixteen bindings have `contextOnly: true`: they use a related background, later outcome, or parallel comparison rather than a direct depiction of the exact sub-event. Their per-step captions explicitly identify that distinction. They remain candidates for more specific future curation, particularly Arusha negotiations, Angola's ceasefire, and the early Green Belt Movement. Do not silently relabel these as contemporary scene photographs.

Each imported JPEG remains under the license shown on its source record. Technical changes are resizing and JPEG re-encoding only. Source pages preserve fuller collection and rights information. No private teaching-file paths are included in the public manifest.
