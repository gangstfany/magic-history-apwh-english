import unittest,json
from english_content import process_js,process_html,walk_json,js_tokens
class EnglishBuildTests(unittest.TestCase):
 def test_strings_preserve_quotes_and_code(self):
  source="const id='u3_main';const name='中文';const rx=/['\"]/g; // 中文\n"
  translated=process_js(source,lambda s:"A student's words")
  self.assertIn("id='u3_main'",translated);self.assertIn('"A student\'s words"',translated);self.assertIn('// 中文',translated)
 def test_template_keeps_expressions(self):
  source='const label=`中文${value + 1}中文`;'
  self.assertEqual(process_js(source,lambda s:'English'),'const label=`English${value + 1}English`;')
 def test_nested_templates(self):
  source='const label=`中文${okay ? `中文${id}` : "中文"}中文`;'
  result=process_js(source,lambda s:'English')
  self.assertEqual(result,'const label=`English${okay ? `English${id}` : "English"}English`;')
 def test_html_preserves_styles_and_layout(self):
  source='<html lang="zh-CN"><style>/* 中文 */div > span{color:red}</style><h2>中文</h2><script>const s="中文";</script></html>'
  output=process_html(source,lambda s:'English')
  self.assertIn('<style>/* 中文 */div > span{color:red}</style>',output);self.assertIn('<h2>English</h2>',output);self.assertIn('const s="English"',output);self.assertIn('lang="en"',output)
 def test_canonical_ids_survive_json_translation(self):
  record={'id':'u3_main','stops':[1,2],'title':'中文'}
  self.assertEqual(walk_json(record,lambda s:'English' if s=='中文' else s),{'id':'u3_main','stops':[1,2],'title':'English'})
if __name__=='__main__':unittest.main()

class ParserRegressionTests(unittest.TestCase):
 def test_quoted_pattern_in_regexp_remains_code(self):
  for source in ['const r = () => /"中文"/;', 'if (value) /"中文"/.test(value);']:
   self.assertEqual(process_js(source,lambda s:'English'),source)
 def test_mixed_quote_attributes(self):
  source='<img alt="John\'s 中文" data-label="中文">'
  self.assertEqual(process_html(source,lambda s:"John's English" if "John" in s else 'English'),'<img alt="John&#x27;s English" data-label="English">')
 def test_template_cannot_close_inline_script(self):
  self.assertNotIn('</script',process_js('const s=`中文`;',lambda s:'</script>'))

class IndependentCoverageRegressions(unittest.TestCase):
 def test_greater_than_inside_display_text(self):
  self.assertEqual(process_html('<p>士 > 商</p>',lambda s:'scholars > merchants'),'<p>scholars &gt; merchants</p>')
 def test_css_display_content_only(self):
  from english_content import process_css
  self.assertEqual(process_css('/* 中文 */a::after{content:"中文"}',lambda s:'English'),'/* 中文 */a::after{content:"English"}')

class EnglishTypographyTests(unittest.TestCase):
 def test_translated_prose_does_not_join_highlighted_names(self):
  self.assertEqual(process_html('<p><span>Islam</span>向北传播</p>',lambda s:'spread north'),'<p><span>Islam</span> spread north</p>')
