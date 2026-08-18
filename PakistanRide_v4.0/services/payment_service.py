from datetime import datetime
from secrets import token_hex
from database.database import connect
METHODS=['Cash','Wallet','Card Demo','Bank Transfer Demo']
def create_payment(ride_id,user_id,amount,method):
 if method not in METHODS: raise ValueError('Unsupported payment method')
 status='Paid' if method=='Cash' else 'Pending'; ref=f'PR-{datetime.now():%Y%m%d}-{token_hex(4).upper()}'
 c=connect(); cur=c.execute('INSERT INTO payments(ride_id,user_id,amount,method,status,reference) VALUES(?,?,?,?,?,?)',(ride_id,user_id,amount,method,status,ref)); c.execute('UPDATE rides SET payment_status=?,payment_method=? WHERE id=?',(status,method,ride_id)); c.commit(); pid=cur.lastrowid; c.close(); return pid,ref,status
def list_payments(uid):
 c=connect(); rows=c.execute('SELECT * FROM payments WHERE user_id=? ORDER BY id DESC',(uid,)).fetchall(); c.close(); return [dict(x) for x in rows]
