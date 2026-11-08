"""Apply source-addressed legacy copy corrections without moving events or pins."""
import html,json,re,hashlib
from collections import Counter
from pathlib import Path

ENTRY=re.compile(r'(<div class="entry[^\"]*"[^>]*>\s*<div class="entry-top">)(.*?)(</div>\s*<div class="trig">)(.*?)(</div>\s*</div>)',re.S)
def apply_legacy_events(world,ledger_path):
    data=json.loads(Path(ledger_path).read_text())
    changes={r['sourceId']:r for r in data['revisions']}
    if len(changes)!=len(data['revisions']):raise ValueError('Duplicate reviewed source ID')
    counts=Counter();applied=set()
    def amend(m):
        num=re.search(r'<span class="citynum"[^>]*>(\d+)</span>',m[2])
        if not num:raise ValueError('Legacy entry has no pin')
        pin=num[1];key=pin+':'+str(counts[pin]);counts[pin]+=1
        revision=changes.get(key)
        if not revision:return m[0]
        if revision['pin']!=pin:raise ValueError('Moving a pin would invalidate canonical identities: '+key)
        if hashlib.sha256(m[4].encode()).hexdigest()!=revision['sourceBodySha256']:raise ValueError('Source content drift: '+key)
        year=re.search(r'(<span class="yr">)(.*?)(</span>)',m[2])
        if not year or html.unescape(year[2])!=revision['oldYear']:raise ValueError('Source date drift: '+key)
        top=m[2][:year.start(2)]+html.escape(revision['year'])+m[2][year.end(2):]
        applied.add(key)
        return m[1]+top+m[3]+revision['html']+m[5]
    result=ENTRY.sub(amend,world)
    if set(changes)!=applied:raise ValueError('Missing reviewed entries: '+str(set(changes)-applied))
    # Correct a reviewed unit assignment while retaining the public source/event ID.
    for row in changes.values():
        move=row.get('unitCorrection')
        if not move:continue
        for unit,remove in [(move['from'],True),(move['to'],False)]:
            pattern=r'('+re.escape(unit)+r':\s*\[)([^\]]+)(\])'
            found=re.search(pattern,result)
            if not found:raise ValueError('Missing unit membership '+unit)
            members=json.loads('['+found[2]+']')
            if remove:
                if row['sourceId'] not in members:raise ValueError('Missing old unit assignment')
                members.remove(row['sourceId'])
            else:
                if row['sourceId'] in members:raise ValueError('Duplicate new unit assignment')
                members.append(row['sourceId'])
            result=result[:found.start(2)]+json.dumps(members,separators=(',',':'))[1:-1]+result[found.end(2):]
    return result
