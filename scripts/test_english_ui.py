import unittest
from english_ui import normalize_ui_copy
class EnglishUICopyTests(unittest.TestCase):
 def test_step_ordinals_do_not_repeat_the_noun(self):
  self.assertEqual(normalize_ui_copy('Unit ${unit} · Step ${step+1} step</span>'),'Unit ${unit} · Step ${step+1}</span>')
  self.assertEqual(normalize_ui_copy('Step ${i+1} / ${total} steps · city'),'Step ${i+1} / ${total} · city')
 def test_route_progress_uses_the_same_counter_pattern(self):
  self.assertEqual(normalize_ui_copy('Stop ${i + 1} of ${route.stops.length} stops</div>'),'Stop ${i + 1} / ${route.stops.length}</div>')
 def test_return_from_trade_means_the_saved_causal_step(self):
  self.assertEqual(normalize_ui_copy('← Return to stop ${chainRouteContext.step+1} step'),'← Return to step ${chainRouteContext.step+1}')
 def test_favorite_subtitles_do_not_append_an_extra_step(self):
  self.assertEqual(normalize_ui_copy('subtitle:c.name+" · Step "+(i+1)+" step",unit:c.unit'),'subtitle:c.name+" · Step "+(i+1),unit:c.unit')
  self.assertEqual(normalize_ui_copy('subtitle:destination.name+" · Step "+(target.step+1)+" step"'),'subtitle:destination.name+" · Step "+(target.step+1)')
 def test_start_quiz_is_a_clear_action_with_a_bounded_question_count(self):
  self.assertEqual(normalize_ui_copy('>Practice quiz<span class="rc-count">10 questions per set</span>'),'>Start quiz<span class="rc-count">Up to 10 questions</span>')
 def test_start_quiz_preserves_spacing_after_its_icon(self):
  self.assertEqual(normalize_ui_copy('</span> Practice quiz<span class="rc-count">10 questions per set</span>'),'</span> Start quiz<span class="rc-count">Up to 10 questions</span>')
 def test_short_labels_and_hint_keep_existing_tags_and_ids(self):
  self.assertEqual(normalize_ui_copy('<button id="trade">Trade Routes and Exchange</button>'),'<button id="trade">Trade & exchange</button>')
  self.assertEqual(normalize_ui_copy('<button data-quiz-action="exit">Exit practice</button>'),'<button data-quiz-action="exit">Back to practice</button>')
 def test_history_numbers_identifiers_and_source_links_are_untouched(self):
  text='{"id":"u4_main:step:1","evidence":"The first step did not cause the second. Mortality was 10–15 percent.","source":"https://example.org/step1"}'
  self.assertEqual(normalize_ui_copy(text),text)
 def test_map_stop_labels_are_not_called_causal_steps(self):
  self.assertEqual(normalize_ui_copy('Step ${routeMode.i+1} / ${p.sites.length} stop'),'Stop ${routeMode.i+1} / ${p.sites.length}')
  self.assertEqual(normalize_ui_copy('Step ${n.index+1} stop: city'),'Stop ${n.index+1}: city')
 def test_full_chain_count_is_idempotent(self):
  text='Full chain · ${route.stops.length} step'
  once=normalize_ui_copy(text)
  self.assertEqual(once,'Full chain · ${route.stops.length} steps')
  self.assertEqual(normalize_ui_copy(once),once)
 def test_clean_copy_is_idempotent(self):
  text='Step ${i+1} / ${total} · Trade & exchange'
  self.assertEqual(normalize_ui_copy(normalize_ui_copy(text)),text)
