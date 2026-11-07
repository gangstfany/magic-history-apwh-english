      // Canonical records, independent of current filters or rendered cards.
      getFavoriteItems: () => [
        ...Array.from({length:9}, (_,i) => window['APWH_U'+(i+1)+'_LOCATION_STUDY'])
          .flatMap(api => api.records.map(r => ({id:r.id,kind:'study-point',title:r.title,subtitle:r.dateLabel,unit:api.unitId}))),
        ...timelineEvents.map(e => ({id:e.key,kind:'event',title:e.titleEn || e.titleZh,subtitle:e.yr,unit:e.unit})),
        ...CHAINS.flatMap(c => c.stops.map((_,i) => ({id:c.id+(c.refinement?':r'+c.refinement.version:'')+':step:'+i,kind:'chain',title:c.labels[i],subtitle:c.name+' · 第 '+(i+1)+' 环',unit:c.entryUnit || c.units?.[0] || ''}))),
        ...CHAINS.flatMap(c => (c.refinement?.legacyFavoriteTargets || []).flatMap((target,i) => {
          const destination=target&&CHAINS.find(x=>x.id===target.chain);
          return destination&&destination.labels[target.step]?[{id:c.id+':step:'+i,kind:'chain',title:destination.labels[target.step],subtitle:destination.name+' · 第 '+(target.step+1)+' 环',unit:destination.entryUnit || destination.units?.[0] || ''}]:[];
        })),
      ],
      openFavorite: item => {
        if (!item || typeof item.id !== 'string') return false;
        if (item.kind === 'study-point') {
          const api = Array.from({length:9},(_,i)=>window['APWH_U'+(i+1)+'_LOCATION_STUDY']).find(a=>a.getById(item.id));
          const record = api?.getById(item.id);
          if (!record) return false;
          showLearningView('map'); showMapMode('events'); reset({includeRegion:true}); setPeriod(api.unitId);
          openEventInMap(record.locationNumber, pinRegion(record.locationNumber), record.mainEventKey, {selectEventUnit:true});
          if (!openLocationStudy(record.locationNumber)) return false;
          if (locationStudyState.expandedStudyId !== record.id) toggleLocationStudy(record.id);
          return locationStudyState.expandedStudyId === record.id;
        }
        if (item.kind === 'event') {
          const event = timelineEventByKey.get(item.id), anchor = event?.anchors[0];
          if (!anchor) return false;
          showLearningView('map'); showMapMode('events'); reset({includeRegion:true}); setPeriod(event.unit);
          openEventInMap(anchor.num, anchor.region, event.key, {selectEventUnit:true});
          return selectedTimelineKey === event.key;
        }
        if (item.kind === 'chain') {
          const match = /^(.*?)(?::r(\d+))?:step:(\d+)$/.exec(item.id);
          let chain = match && CHAINS.find(c=>c.id===match[1]), step = match && Number(match[3]);
          if (chain?.refinement) {
            if (match[2] && match[2]!==chain.refinement.version) return false;
            if (!match[2]) {
              const target=chain.refinement.legacyFavoriteTargets?.[step];
              if (!target) return false;
              chain=CHAINS.find(c=>c.id===target.chain);step=target.step;
            }
          } else if (match?.[2]) return false;
          if (!chain || !Number.isSafeInteger(step) || step >= chain.stops.length) return false;
          showLearningView('map'); reset({includeRegion:true});
          showLearningView('chain'); enterRouteMode(chain.id); goToStop(step);
          return routeMode?.route.id === chain.id && routeMode.i === step;
        }
        return false;
      },
