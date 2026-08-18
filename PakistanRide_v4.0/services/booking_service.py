from datetime import datetime
from database.database import connect
from services.fare_service import estimate_fare
def create_booking(uid,t,pickup,dest,km,mins):
    fare=estimate_fare(t,km,mins); c=connect(); cur=c.execute('INSERT INTO rides(user_id,ride_type,pickup,destination,distance_km,duration_min,fare,status,requested_at) VALUES(?,?,?,?,?,?,?,?,?)',(uid,t,pickup,dest,km,mins,fare,'Searching Driver',datetime.now().isoformat(timespec='seconds'))); rid=cur.lastrowid
    d=c.execute("SELECT * FROM drivers WHERE vehicle_type=? AND status='Available' ORDER BY rating DESC LIMIT 1",(t,)).fetchone()
    if not d:d=c.execute("SELECT * FROM drivers WHERE status='Available' ORDER BY rating DESC LIMIT 1").fetchone()
    if d:c.execute("UPDATE rides SET driver_id=?,status='Driver Assigned' WHERE id=?",(d['id'],rid));c.execute("UPDATE drivers SET status='Busy' WHERE id=?",(d['id'],))
    c.commit();c.close();return rid,fare,dict(d) if d else None
def list_user_rides(uid):
    c=connect();r=c.execute('SELECT r.*,d.name driver_name FROM rides r LEFT JOIN drivers d ON d.id=r.driver_id WHERE r.user_id=? ORDER BY r.id DESC',(uid,)).fetchall();c.close();return [dict(x) for x in r]
def complete_ride(rid):
    c=connect();d=c.execute('SELECT driver_id FROM rides WHERE id=?',(rid,)).fetchone();c.execute("UPDATE rides SET status='Ride Completed',completed_at=? WHERE id=?",(datetime.now().isoformat(timespec='seconds'),rid));
    if d and d['driver_id']:c.execute("UPDATE drivers SET status='Available',total_rides=total_rides+1 WHERE id=?",(d['driver_id'],))
    c.commit();c.close()
