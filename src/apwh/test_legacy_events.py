import html,json,re,unittest
from pathlib import Path
from legacy_events import apply_legacy_events,ENTRY
from enhance_maps import enhance_maps
HERE=Path(__file__).resolve().parent
class LegacyReviewTests(unittest.TestCase):
 def setUp(self):
  self.source=html.unescape(re.search(r'id="worldMapFrame"[^>]*srcdoc="([^"]*)"',(HERE/'source-map-snapshot.html').read_text())[1])
  self.source=enhance_maps(self.source)
  self.revisions=json.loads((HERE/'legacy-event-revisions.json').read_text())['revisions']
 def test_review_applies_to_public_builder(self):
  built=(HERE.parents[1]/'world-map.html').read_text()
  self.assertTrue('Some voyages had exceptionally high mortality' in built, 'Reviewed mortality must reach the published builder')
  self.assertTrue('King Afonso was a ruler of Kongo, a separate kingdom.' in built)
  self.assertTrue('not Afonso’s court' in html.unescape(built))
 def test_corrections_keep_every_pin_and_event_in_its_original_position(self):
  changed=apply_legacy_events(self.source,HERE/'legacy-event-revisions.json')
  pin=lambda s:re.findall(r'<span class="citynum"[^>]*>(\d+)</span>',s)
  self.assertEqual(len(ENTRY.findall(self.source)),288)
  self.assertEqual(pin(changed),pin(self.source))
  self.assertEqual(len(ENTRY.findall(changed)),288)
  for row in self.revisions:self.assertIn(row['html'],changed)
 def test_every_change_records_its_evidence_and_rationale(self):
  for r in self.revisions:
   self.assertTrue(r['reason'],r['sourceId']);self.assertTrue(r['sources'],r['sourceId'])
   for src in r['sources']:
    for n in src.get('physicalPages',[]):self.assertTrue(1<=n<=834)
 def test_content_drift_is_rejected_even_if_the_date_has_not_changed(self):
  target=next(m for m in ENTRY.finditer(self.source) if 'Abbasid' in m[4])
  changed=self.source[:target.start(4)]+target[4]+' '+self.source[target.end(4):]
  with self.assertRaisesRegex(ValueError,'Source content drift'):apply_legacy_events(changed,HERE/'legacy-event-revisions.json')
 def test_sixteenth_century_silver_tax_is_in_the_appropriate_unit(self):
  changed=apply_legacy_events(self.source,HERE/'legacy-event-revisions.json')
  unit=lambda name:json.loads('['+re.search(name+r':\s*\[([^\]]+)\]',changed)[1]+']')
  self.assertNotIn('5:6',unit('u2'))
  self.assertIn('5:6',unit('u4'))
 def test_date_drift_is_rejected_before_silent_wrong_event_correction(self):
  original=self.source.replace('1500–1600','1501–1601',1)
  with self.assertRaisesRegex(ValueError,'Source date drift'):apply_legacy_events(original,HERE/'legacy-event-revisions.json')
if __name__=='__main__':unittest.main()
