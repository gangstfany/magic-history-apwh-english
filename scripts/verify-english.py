"""Verify full display coverage plus canonical course and media parity."""
from pathlib import Path
import json,re,sys,os
from html.parser import HTMLParser
from english_content import inventory,CJK
root=Path(__file__).resolve().parents[1];site=Path(os.environ.get('APWH_ENGLISH_SITE',root/'_site'))
manifest=json.loads((site/'english-edition.json').read_text());assert manifest['status']=='complete','Incomplete local previews cannot be published'
remaining=inventory(site);assert not remaining,'Untranslated display strings remain: '+str(list(remaining)[:4])
source=json.loads((root/'src/apwh/causal-chains.json').read_text());expected=[c for c in source if c['units']!=['u1'] and(c['units']==['u2'] or c.get('refinement'))]
translated=json.loads((site/'assets/apwh-u2-visual/chains.json').read_text());assert len(expected)==len(translated)
def same_structure(old,new,path=''):
 assert type(old)==type(new),path
 if isinstance(old,dict):
  assert old.keys()==new.keys(),path
  for key in old:same_structure(old[key],new[key],path+'/'+key)
 elif isinstance(old,list):
  assert len(old)==len(new),path
  for i,(a,b) in enumerate(zip(old,new)):same_structure(a,b,path+'/'+str(i))
 elif not isinstance(old,str) or not CJK.search(old):assert old==new,path
for a,b in zip(expected,translated):same_structure(a,b,a['id'])
# The corrected study-point records already contain English teaching content.
source_units=json.loads((root/'src/apwh/content-corrected.json').read_text())
world=(site/'world-map.html').read_text();units=[]
for match in re.finditer(r'\(function publishUnit\d+LocationStudy\(root\)\s*\{\s*[\'\"]use strict[\'\"];\s*const data = (\{[^\n]+\});',world):
 units.append(json.loads(match[1]))
assert len(units)==9,('unit APIs',len(units))
for old,new in zip(source_units,units):
 assert old['unit']==new['unit'];assert [r['id'] for r in old['records']]==[r['id'] for r in new['records']]
 for a,b in zip(old['records'],new['records']):
  for key in ['mainEventKey','locationNumber','topicCodes','causeStudyPointIds','effectStudyPointIds','relatedStudyPointIds']:
   assert a.get(key)==b.get(key),(a['id'],key)
for name in ['CHAINS']:
 marker='const '+name+' = '
 original=(root/'world-map.html').read_text().split(marker,1)[1].lstrip();built=world.split(marker,1)[1].lstrip()
 a=json.JSONDecoder().raw_decode(original)[0];b=json.JSONDecoder().raw_decode(built)[0];same_structure(a,b,name)
 if name=='CHAINS':print(f'Canonical parity: {len(a)} chains / {sum(len(c["stops"]) for c in a)} steps unchanged')
route_pattern=r"\{ id: [\"']([^\"']+)[\"'][^\n]*stops: (\[[0-9, ]+\])"
assert re.findall(route_pattern,(root/'world-map.html').read_text())==re.findall(route_pattern,world),'Trade-route IDs/stops'
assert 'lang="en"' in (site/'index.html').read_text();assert 'lang="en"' in world
print(f'English verified: 9 Unit APIs; {sum(len(u["records"]) for u in units)} study cards; {len(translated)} visible chains; no untranslated display strings')

class VisibleHTML(HTMLParser):
 def __init__(self):super().__init__();self.hidden=0;self.tags=[];self.ids=[];self.bad=[]
 def handle_starttag(self,tag,attrs):
  self.tags.append(('start',tag));self.ids.extend(value for name,value in attrs if name=='id')
  if tag in ['script','style']:self.hidden+=1
  for name,value in attrs:
   if value and name in ['aria-label','aria-description','title','placeholder','alt'] and CJK.search(value):self.bad.append((name,value))
 def handle_endtag(self,tag):
  self.tags.append(('end',tag))
  if tag in ['script','style']:self.hidden=max(0,self.hidden-1)
 def handle_data(self,text):
  if not self.hidden and CJK.search(text):self.bad.append(('text',text))
for name in ['index.html','world-map.html']:
 old=VisibleHTML();new=VisibleHTML();old.feed((root/name).read_text());new.feed((site/name).read_text());assert old.tags==new.tags,(name,'layout tags');assert old.ids==new.ids,(name,'element IDs');assert not new.bad,(name,new.bad[:3])
print('Independent HTML scan: no Chinese display text; identical element order and IDs')
