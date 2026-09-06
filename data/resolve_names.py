import json as J, urllib.request, time, os
ids=[l.strip() for l in open('owned_ids.txt') if l.strip()]
out=J.load(open('names.json')) if os.path.exists('names.json') else {}
for aid in ids:
    if aid in out: continue
    try:
        req=urllib.request.Request(f'https://store.steampowered.com/api/appdetails?appids={aid}&filters=basic,platforms,categories,genres', headers={'User-Agent':'Mozilla/5.0'})
        d=J.load(urllib.request.urlopen(req,timeout=30)).get(aid,{})
        if d.get('success'):
            x=d['data']; out[aid]={'name':x.get('name'),'type':x.get('type'),'platforms':x.get('platforms'),'categories':[c['description'] for c in x.get('categories',[])],'genres':[g['description'] for g in x.get('genres',[])],'controller':x.get('controller_support')}
        else: out[aid]={'name':None,'note':'no store page'}
    except Exception as e:
        out[aid]={'name':None,'note':str(e)[:60]}; time.sleep(5)
    open('names.json','w').write(J.dumps(out,indent=0)); time.sleep(1.6)
print('done',len(out))
