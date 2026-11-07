const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const chains=JSON.parse(fs.readFileSync(path.join(__dirname,'causal-chains.json'))),byId=Object.fromEntries(chains.map(c=>[c.id,c]));
test('priority units separate incompatible historical processes instead of treating them as adjacent causes',()=>{
 assert.ok(byId.u5_sub_industry,'industrialization retains a complete independent chain');
 assert.ok(byId.u7_sub_asia,'Asian expansion retains its own causal pathway');
 assert.ok(byId.u7_sub_holocaust,'genocide is explained by its own actors and mechanisms');
 assert.ok(byId.u8_sub_decolonization,'decolonization is a complete process, not a stop on the Cold War itinerary');
 assert.doesNotMatch(byId.u5_main.labels.join(' '),/机器|工厂|工业/);
 assert.doesNotMatch(byId.u7_main.labels.join(' '),/Japan|日本|Holocaust|灭绝/);
 assert.doesNotMatch(byId.u8_main.labels.join(' '),/Partition|分治|India|印巴/);
});
test('refined content has no dangling or stale event and source anchors',()=>{
 const selected=chains.filter(c=>c.units.some(u=>/^u[3-9]$/.test(u)));
 assert.ok(selected.every(c=>c.refinement?.version==='20261031'), 'every audited unit is covered');
 for(const c of selected){
  const n=c.stops.length;for(const field of ['labels','evidence','links','stepNotes','stopEvents'])assert.equal(c[field]?.length,n,c.id+' '+field);
  assert.ok(c.stopEvents.every(k=>k===''),c.id+' must not select old events after a rewrite');
  assert.ok(c.labels.every(Boolean)&&c.evidence.every(Boolean)&&c.links.slice(0,-1).every(Boolean));
  assert.ok(c.stepNotes.every(ns=>ns.length&&ns.every(n=>n.text&&n.sources?.length)));
  assert.ok(c.refinement.question&&c.refinement.scope);
  for(const side of ['from','to'])if(c[side]?.chain)assert.ok(byId[c[side].chain],c.id+' seam');
 }
 assert.equal(new Set(chains.map(c=>c.id)).size,chains.length);
});
test('navigation seams explain course order rather than imply universal historical succession',()=>{
 for(const id of ['u3_main','u4_main','u5_main','u6_main','u7_main','u8_main'])assert.match(byId[id].to.summary,/学习|课程/);
});
test('local-source review keeps distinct institutional processes and honest old-favorite destinations',()=>{
 assert.match(byId.u4_sub_company.evidence[0],/East India Company/);
 assert.match(byId.u4_sub_company.evidence[1],/EIC/);
 assert.match(byId.u4_sub_company.evidence[2],/EIC/);
 assert.match(byId.u7_sub_slump.evidence.join(' '),/Brazil/);
 assert.match(byId.u7_sub_slump.evidence[2],/Vargas/);
 assert.doesNotMatch(byId.u7_sub_slump.evidence.join(' '),/Argentina/);
 assert.equal(byId.u9_main.stops[3],65,'pre-Seattle labor example uses Mexican maquiladoras, not the later Dhaka disaster');
 assert.match(byId.u9_main.evidence[3],/1990年代Mexico/);
 assert.match(byId.u9_main.links[3],/不由后来2013/,'2013 disaster cannot be a cause of the 1999 protest');
 assert.ok(byId.u9_sub_rwanda.stops.every(id=>id===83),'Rwandan case uses Kigali rather than Sarajevo');
 assert.equal(byId.u9_sub_unfrozen.refinement.legacyFavoriteTargets[2].chain,'u9_sub_rwanda');
 assert.doesNotMatch(byId.u9_sub_unfrozen.evidence[3],/Rwanda|UNAMIR/,'Bosnia outcome must not silently switch to a different genocide');
 assert.deepEqual(byId.u9_main.refinement.legacyFavoriteTargets[0],{chain:'u9_sub_green_revolution',step:0});
 assert.deepEqual(byId.u9_sub_unfrozen.refinement.legacyFavoriteTargets[0],{chain:'u9_sub_european_integration',step:0},'restored European integration favorite must open its own case, not a UN protection-failure card');
 assert.ok(byId.u9_sub_european_integration.stops.every(id=>id===31));
 assert.match(byId.u9_sub_european_integration.evidence[2],/1973.*1993/);
 assert.equal(byId.u9_sub_unfrozen.refinement.legacyFavoriteTargets[3].chain,'u9_sub_darfur');
 assert.match(byId.u9_sub_darfur.evidence[0],/western Sudan/);
 assert.equal(byId.u8_sub_howwon.refinement.legacyFavoriteTargets[2].chain,'u8_sub_algeria','Algerian independence must open its own case rather than a Ghana governance card');
 for(const c of chains.filter(c=>c.units.some(u=>/^u[3-9]$/.test(u)))){
  assert.ok(c.refinement.localSourceReview,c.id+' must record review status');
  for(const notes of c.stepNotes)assert.ok(notes.some(n=>n.sources.some(s=>/AMSCO/.test(s.title)&&/纸质页.*PDF物理页/.test(s.locator))),c.id+' missing physical/printed page distinction');
 }
 assert.match(byId.u9_sub_voice.stepNotes[0][0].sources[0].locator,/775/,'Arab Spring case must cite the actual local textbook passage');
});
test('the existing compact reader receives refined chains and keeps missing images in a short visual placeholder',()=>{
 const published=JSON.parse(fs.readFileSync(path.join(__dirname,'../../assets/apwh-u2-visual/chains.json')));
 assert.ok(published.some(c=>c.id==='u5_sub_industry'));
 const reader=fs.readFileSync(path.join(__dirname,'../workspace/u2-visual/reader.js'),'utf8');
 assert.match(reader,/本环事件配图待补充/);
});

test('Asian occupation evidence uses the Nanjing map anchor and discloses regional Japan anchors',()=>{
 assert.equal(byId.u7_sub_asia.stops[1],10,'Nanjing evidence must not pan the map to Beijing');
 assert.match(byId.u7_sub_asia.evidence[4],/Edo\/Tokyo.*锚点/);
});
