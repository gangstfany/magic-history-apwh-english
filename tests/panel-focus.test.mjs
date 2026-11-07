import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';
function load(){const window={};vm.runInNewContext(fs.readFileSync(new URL('../src/workspace/panel-focus.js',import.meta.url),'utf8'),{window});return window.APWH_PANEL_FOCUS;}
function button(attrs={},disabled=false){return {tagName:'BUTTON',disabled,tabIndex:0,getAttribute:k=>attrs[k]??null,hasAttribute:k=>Object.hasOwn(attrs,k),focus(){this.focused=true;},closest(){return this;}};}
test('next and selected-step controls regain focus after replacing side-panel markup',()=>{
 const api=load();for(const [attr,value] of [['data-route-action','next'],['data-route-step','3']]){const old=button({[attr]:value}),fresh=button({[attr]:value}),root={contains:e=>e===old,querySelectorAll:()=>[fresh],querySelector:()=>null};const key=api.capture(root,old);api.restore(root,key);assert.equal(fresh.focused,true);}
});
test('a disabled final Next falls back to the current step and outside focus is untouched',()=>{
 const api=load(),old=button({'data-route-action':'next'}),disabled=button({'data-route-action':'next'},true),current=button({'data-route-step':'7'}),root={contains:e=>e===old,querySelectorAll:()=>[disabled],querySelector:()=>current};
 api.restore(root,api.capture(root,old));assert.equal(current.focused,true);assert.equal(disabled.focused,undefined);assert.equal(api.capture(root,button()),null);
});
