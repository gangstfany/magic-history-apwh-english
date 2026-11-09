const test=require('node:test'),assert=require('node:assert/strict');
const {readableScrollTop}=require('./model.js');
const base={scrollTop:0,visibleTop:80,visibleBottom:447,targetTop:447,targetBottom:495,previewHeight:0,gap:12};
test('initial card clears the sticky bottom controls without changing layout',()=>{assert.equal(readableScrollTop(base),60);});
test('expanding a card reveals its beginning with the selected heading',()=>{assert.equal(readableScrollTop({...base,scrollTop:60,targetTop:387,targetBottom:435,previewHeight:96}),156);});
test('a selection already readable does not move',()=>{assert.equal(readableScrollTop({...base,scrollTop:225,targetTop:120,targetBottom:168,previewHeight:96}),225);});
test('previous navigation reveals a row hidden by the sticky tabs',()=>{assert.equal(readableScrollTop({...base,scrollTop:500,targetTop:40,targetBottom:88}),448);});
test('very long content aligns the heading instead of scrolling past it',()=>{assert.equal(readableScrollTop({...base,scrollTop:300,targetTop:200,targetBottom:600,previewHeight:96}),408);});
test('long explanation previews are capped to the space beside a readable heading',()=>{assert.equal(readableScrollTop({...base,targetTop:300,targetBottom:348,previewHeight:1000}),208);});
