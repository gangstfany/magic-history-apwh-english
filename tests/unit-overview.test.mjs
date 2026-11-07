import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source=()=>fs.readFileSync(new URL('../src/workspace/unit-overview.js',import.meta.url),'utf8');
function load(){const root={};vm.runInNewContext(source(),{window:root});return root.APWH_UNIT_OVERVIEW;}
for(let n=1;n<=9;n++)test(`Unit ${n} overview uses existing location records and bookends`,()=>{
 const root={};root.window=root;vm.runInNewContext(fs.readFileSync(new URL(`../data/apwh-u${n}-location-study.js`,import.meta.url),'utf8'),root);
 const api=root[`APWH_U${n}_LOCATION_STUDY`];const html=load().render(api);
 assert.match(html,new RegExp(`UNIT 0${n}`));
 assert.ok(html.includes(api.getUnitCard('context').title));
 assert.ok(html.includes(api.getUnitCard('synthesis').title));
 assert.equal((html.split('data-overview-section="cards"')[1].split('data-overview-section="review"')[0].match(/data-overview-location=/g)||[]).length,api.locationNumbers.filter(x=>api.getByLocation(x).length).length);
 assert.ok(html.includes(`${api.records.length} study points`));
 const groups=load().themeGroups(api);
 for(const record of api.records) assert.ok(groups.some(g=>g.records.some(r=>r.id===record.id)),record.id);
 for(const record of api.records) for(const id of record.themeIds||[]) assert.ok(groups.find(g=>g.id===id)?.records.some(r=>r.id===record.id));
});
test('overview escapes authored text and resets on Unit changes only',()=>{
 const {render,next}=load();
 const api={unitNumber:1,unitId:'u1',records:[],locationNumbers:[],getUnitCard:()=>({title:'<img onerror=x>',summary:'A&B',takeaways:[],prompt:'"hello"',examSkills:[]})};
 const html=render(api);assert.doesNotMatch(html,/<img/);assert.match(html,/&lt;img/);
 let s=next(null,'u1');assert.equal(s.overview,true);s={...s,overview:false};assert.equal(next(s,'u1').overview,false);assert.equal(next(s,'u2').overview,true);
});

test('theme groups cover every authored card without inventing or truncating themes',()=>{
 const root={};root.window=root;vm.runInNewContext(fs.readFileSync(new URL('../data/apwh-u1-location-study.js',import.meta.url),'utf8'),root);
 const api=root.APWH_U1_LOCATION_STUDY;const groups=load().themeGroups(api);
 for(const record of api.records) for(const theme of record.themeIds)assert.ok(groups.find(g=>g.id===theme).records.some(r=>r.id===record.id));
 assert.match(load().render(api),/data-overview-study=/);
});
test('keyboard activation requests the same details as pointer selection',()=>{
 const api=load(),target={closest:()=>({})};
 assert.equal(api.isSelectionIntent({type:'keydown',key:'Enter',target}),true);
 assert.equal(api.isSelectionIntent({type:'keydown',key:' ',target}),true);
 assert.equal(api.isSelectionIntent({type:'keydown',key:'Tab',target}),false);
 assert.equal(api.isSelectionIntent({type:'click',target}),true);
});
test('cross-unit directory navigation dismisses overview after synchronous Unit callbacks',()=>{
 const source=fs.readFileSync(new URL('../src/workspace/index.template.html',import.meta.url),'utf8');
 const start=source.indexOf('  function openHostStudyLocation(unit, number) {');
 const fn=source.slice(start,source.indexOf('\n  }',start)+4);
 let period='',requested=false,overview=true;const data={getByLocation:()=>[{mainEventKey:'event'}]};
 const ctx={requestHomeDetail(){requested=true;},document:{getElementById:()=>({textContent:''})},worldMapFrame:{contentWindow:{APWH_U3_LOCATION_STUDY:data,document:{querySelectorAll:()=>[{querySelector:()=>({textContent:'5'}),dataset:{region:'asia'}}]}}},HOME_STUDY_GLOBAL_BY_UNIT:{u3:'APWH_U3_LOCATION_STUDY'},commitHostSearch(){},syncHomeEvents(){if(requested){overview=false;requested=false;}},renderHostStudyDirectory(){},styleEmbeddedMap(){},homeEvents:{querySelector:()=>null}};
 ctx.hostApi={setLearningView(){ctx.syncHomeEvents();},setPeriod(u){if(u!==period){period=u;overview=true;}ctx.syncHomeEvents();},openEventInMap(){ctx.syncHomeEvents();},openLocationStudy(){return true;}};
 vm.runInNewContext(fn+';openHostStudyLocation("u3","5");',ctx);assert.equal(overview,false);
});
