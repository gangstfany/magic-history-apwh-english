(function(root){
 'use strict';
 const names=[['全球图景','The Global Tapestry','c. 1200–1450'],['交流网络','Networks of Exchange','c. 1200–1450'],['陆上帝国','Land-Based Empires','c. 1450–1750'],['跨洋联系','Transoceanic Interconnections','c. 1450–1750'],['革命','Revolutions','c. 1750–1900'],['工业化的影响','Consequences of Industrialization','c. 1750–1900'],['全球冲突','Global Conflict','c. 1900–present'],['冷战与非殖民化','Cold War and Decolonization','c. 1900–present'],['全球化','Globalization','c. 1900–present']];
 const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const list=xs=>`<ul>${(xs||[]).map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`;
 function next(previous,unit){return previous?.unit===unit?previous:{unit,overview:true};}
 const themeLabels={ENV:'Humans and the Environment · 人类与环境',CDI:'Cultural Developments and Interactions · 文化发展与互动',GOV:'Governance · 治理',ECN:'Economic Systems · 经济体系',SIO:'Social Interactions and Organization · 社会组织',TEC:'Technology and Innovation · 技术与创新'};
 function themeGroups(api){
  const groups=new Map();
  for(const record of api.records)for(const id of new Set(record.themeIds?.length?record.themeIds:['OTHER'])){
   if(!groups.has(id))groups.set(id,{id,label:themeLabels[id]||(id==='OTHER'?'Other learning topics · 其他学习主题':id),records:[]});
   groups.get(id).records.push(record);
  }
  return [...groups.values()];
 }
 function isSelectionIntent(event){return (event.type==='click'||(event.type==='keydown'&&(event.key==='Enter'||event.key===' ')))&&!!event.target?.closest?.('.pin-group,[data-event-key]');}
 function render(api){
  const n=api.unitNumber,meta=names[n-1];if(!meta)return '';
  const context=api.getUnitCard('context'),review=api.getUnitCard('synthesis');if(!context||!review)return '';
  const locations=api.locationNumbers.filter(x=>api.getByLocation(x).length);
  const themes=themeGroups(api).map(group=>`<details class="unit-overview-theme"><summary>${esc(group.label)} <span class="unit-overview-count">${group.records.length}</span></summary><div>${group.records.map(record=>`<button type="button" class="unit-overview-place" data-overview-study="${esc(record.id)}" data-overview-location="${esc(record.locationNumber)}"><span><strong>${esc(record.title)}</strong><small>${esc(api.locationName(record.locationNumber))} · ${esc(record.dateLabel)} →</small></span></button>`).join('')}</div></details>`).join('');
  const places=locations.map(number=>{const records=api.getByLocation(number);return `<button class="unit-overview-place" data-overview-location="${esc(number)}"><span class="unit-overview-number">${esc(number)}</span><span><strong>${esc(api.locationName(number))}</strong><small>${records.length} study points →</small></span></button>`}).join('');
  return `<section class="unit-overview" data-unit-overview="${esc(api.unitId)}" aria-label="Unit ${n} 学习概览"><p class="unit-overview-kicker">UNIT ${String(n).padStart(2,'0')} / STUDY POINTS</p><h2 tabindex="-1" data-overview-title>${esc(meta[0])}</h2><p class="unit-overview-subtitle">${esc(meta[1])} · ${esc(meta[2])}</p><p class="unit-overview-intro">点击地图或上方 Study points 的 ${locations.length} 处地点，查看相关知识卡。</p><details data-overview-section="context"><summary>Unit 背景与联系</summary><div class="unit-overview-body"><h3>${esc(context.title)}</h3><p>${esc(context.summary)}</p>${list(context.takeaways)}</div></details><details data-overview-section="themes"><summary>按学习主题浏览 · 比较与论证</summary><div class="unit-overview-body"><p>${esc(context.prompt)}</p><p class="unit-overview-meta">按现有知识卡的课程主题分组；一张卡可能出现在多个主题中，数量不相加。</p>${themes}<h3>Exam skills</h3><p>${[...new Set([...(context.examSkills||[]),...(review.examSkills||[])])].map(esc).join(' · ')}</p></div></details><details data-overview-section="cards"><summary>完整知识卡列表 · 按地点浏览 <span class="unit-overview-count">${api.records.length}</span></summary><div class="unit-overview-body"><p class="unit-overview-meta">${locations.length} places · ${api.records.length} study points</p>${places}</div></details><details data-overview-section="review"><summary>Unit 总复习与论证提示</summary><div class="unit-overview-body"><h3>${esc(review.title)}</h3><p>${esc(review.summary)}</p><p>${esc(review.prompt)}</p>${list(review.takeaways)}</div></details></section>`;
 }
 root.APWH_UNIT_OVERVIEW=Object.freeze({render,next,themeGroups,isSelectionIntent});
})(window);
