"""Build the complete English edition; fail closed on any untranslated display string."""
from pathlib import Path
import sys,runpy,json,hashlib,shutil,argparse,os,re
from english_content import inventory,files,process_file,CJK
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);parser.add_argument('--allow-incomplete',action='store_true',help='Local review only: retain untranslated strings and write a gap report; never use for deployment');args=parser.parse_args()
runpy.run_path(str(ROOT/'scripts/build-site.py'),run_name='__main__')
out=ROOT/'_site'
# Only the pinned source and declared generated packages may enter this edition.
source_files=json.loads((ROOT/'ENGLISH-SOURCE-FILES.json').read_text())
allowed={'index.html','world-map.html','module-bridge.mjs','module-protocol.mjs','favorites.mjs','.nojekyll'}
for name in source_files:
 if name.startswith(('assets/','data/')):allowed.add(name)
 for package in ['u1-comparison','u2-visual']:
  prefix='src/workspace/'+package+'/'
  if name.startswith(prefix) and not name.endswith(('.md','.test.cjs')):allowed.add('assets/apwh-'+package+'/'+name[len(prefix):])
allowed.update(['assets/apwh-u2-visual/chains.json','assets/apwh-u1-integration.js','assets/apwh-unit-overview.js','assets/apwh-unit-overview.css','assets/apwh-panel-focus.js'])
if args.output_dir:
 target=args.output_dir.resolve()
 if target==ROOT or ROOT in target.parents and target!=out.resolve():raise SystemExit('Output must be _site or outside source checkout')
 if target.exists():shutil.rmtree(target)
 target.mkdir(parents=True)
 for relative in allowed:
  source=out/relative
  if source.is_file():
   dest=target/relative;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
 out=target
else:
 for path in sorted(out.rglob('*'),reverse=True):
  if path.is_file() and str(path.relative_to(out)) not in allowed:path.unlink()
baseline=inventory(out)
catalog={};conflicts=[]
for name in ['chains-u1-u3.json','chains-u4-u6.json','chains-u7-u9.json','world-content.json','catalogue.json','ui.json','corrections.json']:
 path=ROOT/'translations'/name
 if not path.exists():continue
 entries=json.loads(path.read_text())
 for source,english in entries.items():
  if not isinstance(english,str) or not english.strip() or CJK.search(english):raise ValueError('Invalid translation in '+name+': '+source[:80])
  if source in catalog and catalog[source]!=english:conflicts.append({'source':source,'prior':catalog[source],'selected':english,'catalog':name})
  catalog[source]=english
missing={s:paths for s,paths in baseline.items() if s not in catalog}
report={'language':'en','sourceStrings':len(baseline),'translatedStrings':len(baseline)-len(missing),'missingStrings':missing,'overlappingTranslations':conflicts}
(ROOT/'translations/coverage-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if missing and not args.allow_incomplete:raise SystemExit(f'English build blocked: {len(missing)} untranslated display strings. See translations/coverage-report.json')
images={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.suffix.lower() in ['.jpg','.jpeg','.png','.webp','.svg']}
for path in files(out):
 text=process_file(path,lambda s:catalog.get(s,s))
 # English ordinals and totals use one noun, rather than Chinese prefix/suffix order.
 text=re.sub(r'Step (\$\{[^}]+\})( / \$\{[^}]+\})? step(?=[: ·`])',lambda m:'Step '+m[1]+(m[2] or ''),text)
 text=text.replace('Full chain · ${route.stops.length} step','Full chain · ${route.stops.length} steps')
 text=text.replace('>Comparison theme<','>Theme<').replace('>Comparison group<','>Case pair<').replace('EVENT IN FOCUS / Event image','EVENT IN FOCUS').replace('Trade routes and exchange</button>','Trade & exchange</button>')
 text=text.replace('Click a region to expand its content; click again to collapse. Click “Comparison and explanation” below to view it in a map popup.','Select a case to read more.')
 path.write_text(text)
remaining=inventory(out)
if remaining and not args.allow_incomplete:raise SystemExit('English build blocked: translation pass left '+str(len(remaining))+' CJK display strings')
for relative,digest in images.items():assert hashlib.sha256((out/relative).read_bytes()).hexdigest()==digest,relative
(out/'display-translations.json').write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+'\n')
manifest=json.loads((ROOT/'ENGLISH-EDITION.json').read_text());manifest.update({'status':'incomplete-local-preview' if remaining else 'complete','translatedDisplayStrings':len(baseline)-len(missing),'remainingDisplayStrings':len(remaining),'imageCount':len(images)})
(out/'english-edition.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'English display coverage: {len(baseline)-len(missing)}/{len(baseline)}; remaining: {len(remaining)}; {len(images)} unchanged images')
