import json,re
from pathlib import Path
for p in (Path(__file__).resolve().parent.parent/'data'/'pakistan').glob('*.json'):
 a=json.loads(p.read_text(encoding='utf-8'));seen=set();o=[]
 for r in a:
  r['name']=re.sub(r'\s+',' ',r.get('name','').strip());k=r['name'].lower()
  if r['name'] and k not in seen:seen.add(k);o.append(r)
 p.write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
