/* Preserve logical navigation when the iframe's learning panel is mirrored. */
(function(root){
 const attributes=['data-route-action','data-route-step','data-route-go','data-chain-pick','data-quiz-action','data-quiz-start','data-quiz-period','data-quiz-theme','data-quiz-term'];
 function capture(panel,active){
  if(!active||!panel.contains(active))return null;
  const control=active.closest?.('button,select');if(!control)return null;
  for(const attribute of attributes)if(control.hasAttribute(attribute))return {attribute,value:control.getAttribute(attribute)};
  return null;
 }
 function restore(panel,key){
  if(!key)return false;
  const control=[...panel.querySelectorAll(`[${key.attribute}]`)].find(e=>e.getAttribute(key.attribute)===key.value&&!e.disabled);
  const target=control||panel.querySelector('.rt-stop.now,[data-quiz-action="next"]:not(:disabled),.qz-stem,.rt-top h2,.qz-title');
  if(!target)return false;if(!['BUTTON','SELECT'].includes(target.tagName))target.tabIndex=-1;
  target.focus({preventScroll:true});return true;
 }
 root.APWH_PANEL_FOCUS=Object.freeze({capture,restore});
})(window);
