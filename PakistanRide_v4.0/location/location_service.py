import re
from database.database import connect
def normalize(x): return re.sub(r'\s+',' ',re.sub(r'[^\w\s]',' ',(x or '').lower())).strip()
def search_locations(q,limit=30):
    q=normalize(q);c=connect();r=c.execute('SELECT * FROM locations WHERE normalized LIKE ? ORDER BY name LIMIT ?',('%'+q+'%',limit)).fetchall();c.close();return [dict(x) for x in r]
