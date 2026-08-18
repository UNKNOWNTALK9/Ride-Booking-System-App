from database.database import connect
def estimate_fare(t,km,mins,peak=False):
    c=connect(); r=c.execute('SELECT * FROM ride_types WHERE name=?',(t,)).fetchone(); c.close()
    if not r: raise ValueError('Unknown ride type')
    f=r['base_fare']+r['per_km']*max(0,km)+r['per_minute']*max(0,mins); return round(f*(1.25 if peak else 1),2)
