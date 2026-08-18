import json
from pathlib import Path
from database.database import connect
from location.location_service import normalize
ROOT=Path(__file__).resolve().parent.parent
def run():
 c=connect()
 for fn,level in [('provinces.json','province'),('cities.json','city'),('areas.json','area'),('landmarks.json','landmark')]:
  p=ROOT/'data'/'pakistan'/fn
  if p.exists():
   for r in json.loads(p.read_text(encoding='utf-8')): c.execute('INSERT OR IGNORE INTO locations(level,name,name_ur,normalized,province,division,district,tehsil,city,category) VALUES(?,?,?,?,?,?,?,?,?,?)',(level,r['name'],r.get('name_ur',''),normalize(r['name']),r.get('province',''),r.get('division',''),r.get('district',''),r.get('tehsil',''),r.get('city',''),r.get('category','')))
 c.commit();c.close()
