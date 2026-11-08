const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'../..');
function exitHarness(options){
 const page=fs.readFileSync(path.join(root,'world-map.html'),'utf8');
 const start=page.indexOf('  function exitQuiz('),end=page.indexOf('\n  function renderQuiz(',start);
 const calls=[];let restored=false;
 const ctx={quizMode:{q:{}},activeLearningView:'practice',eventPanel:{querySelector:()=>null,classList:{remove(){}},innerHTML:'quiz'},eventEmpty:{style:{}},svg:{querySelectorAll:()=>[]},resetRegionToBaseline(){},restoreFilters(){restored=true;calls.push('restore');},eventZone:{setAttribute(){}},renderPicker(kind){assert.equal(restored,true,'restore filters before building the practice menu');calls.push(kind);},syncLearningTabs(){calls.push('tabs');},syncMapModeTabs(){}};
 vm.runInNewContext(page.slice(start,end)+'\nexitQuiz('+JSON.stringify(options)+');',ctx);
 return {ctx,calls};
}
test('Exit practice returns to the practice menu after restoring its filters',()=>{const {ctx,calls}=exitHarness();assert.equal(ctx.quizMode,null);assert.equal(ctx.activeLearningView,'practice');assert.deepEqual(calls,['restore','quiz','tabs']);});
test('leaving practice for another module does not reopen its menu',()=>{assert.deepEqual(exitHarness({returnToPractice:false}).calls,['restore']);});
test('Timbuktu legacy event describes diffusion into West Africa',()=>{const c=JSON.parse(fs.readFileSync(path.join(root,'translations/world-content.json')));const value=c['沿trans-Saharan北传 — Timbuktu成伊斯兰学术圣地,但西非人多保留传统信仰'];assert.match(value,/into West Africa/);assert.doesNotMatch(value,/spread north/);});
test('both Sundiata legacy displays retain the textbook qualification',()=>{for(const name of ['world-content.json','chains-u1-u3.json']){const c=JSON.parse(fs.readFileSync(path.join(root,'translations',name)));const matches=Object.entries(c).filter(([k,v])=>k.includes('穆斯林君主')||k.includes('Sundiata 是穆斯林'));assert.ok(matches.length);for(const [,v] of matches)assert.match(v,/Most scholars believe/);}});
