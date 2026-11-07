import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
const root=new URL('../',import.meta.url);
test('independent APWH retains course controls with no account or other course dependencies',()=>{
 const html=fs.readFileSync(new URL('index.html',root),'utf8');assert.match(html,/id="hostPeriod"/);assert.match(html,/id="home-events"/);assert.match(html,/id="worldMapFrame"/);assert.match(html,/data-learning-view="practice"/);
 assert.doesNotMatch(html,/assets\/auth|art-history-map\.html|apush-map\.html/);assert.doesNotMatch(html,/资料与勘误/);
});
test('every unit retains one main chain and source arrays agree',()=>{const c=JSON.parse(fs.readFileSync(new URL('src/apwh/causal-chains.json',root),'utf8'));for(let n=1;n<=9;n++)assert.equal(c.filter(c=>c.entryUnit==='u'+n&&c.tier==='main').length,1);for(const row of c)for(const key of ['labels','evidence','links','stepNotes'])assert.equal(row[key].length,row.stops.length);});
