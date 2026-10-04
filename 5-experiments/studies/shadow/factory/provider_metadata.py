import json,urllib.request
x=json.load(urllib.request.urlopen('https://openrouter.ai/api/v1/models',timeout=30))
for m in x['data']:
    if 'sonnet-4.6' in m['id']:
        print(json.dumps({k:m.get(k) for k in ('id','pricing','supported_parameters','context_length')}))
