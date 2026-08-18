import hashlib,secrets
from database.database import connect
def hash_password(p):
    s=secrets.token_hex(16); return s+'$'+hashlib.sha256((s+p).encode()).hexdigest()
def verify_password(p,x):
    try:s,d=x.split('$',1); return hashlib.sha256((s+p).encode()).hexdigest()==d
    except ValueError:return False
def login(u,p):
    c=connect(); r=c.execute('SELECT * FROM users WHERE username=?',(u.strip(),)).fetchone(); c.close(); return dict(r) if r and verify_password(p,r['password_hash']) else None
def register(name,u,p,phone=''):
    if not name.strip() or not u.strip() or len(p)<6: raise ValueError('Name, username and password (6+ chars) are required.')
    from datetime import datetime
    c=connect()
    try:c.execute('INSERT INTO users(username,password_hash,role,name,phone,created_at) VALUES(?,?,?,?,?,?)',(u.strip(),hash_password(p),'Passenger',name.strip(),phone.strip(),datetime.now().isoformat(timespec='seconds')));c.commit()
    except Exception as e: raise ValueError('Username already exists.') from e
    finally:c.close()
