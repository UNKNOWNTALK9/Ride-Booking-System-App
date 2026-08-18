from datetime import datetime
from database.database import connect
RATES={'Car':(250,55,4,350),'Bike':(100,25,2,120),'Van':(400,75,5,500),'Bus':(700,100,8,800),'Rickshaw':(120,30,2.5,150)}
def baseline(t,km,mins):
 b,k,m,mn=RATES[t]; peak=1.15 if datetime.now().hour in list(range(7,10))+list(range(17,21)) else 1
 return max(mn,(b+km*k+mins*m)*peak)
def predict(t,km,mins):
 km=max(0,float(km)); mins=max(0,float(mins)); base=baseline(t,km,mins); c=connect()
 hist=c.execute("SELECT distance_km,duration_min,fare FROM rides WHERE ride_type=? AND status='Ride Completed' AND distance_km>0 AND duration_min>0 AND fare>0 ORDER BY id DESC LIMIT 500",(t,)).fetchall()
 active=c.execute("SELECT COUNT(*) n FROM rides WHERE ride_type=? AND status NOT IN ('Ride Completed','Cancelled')",(t,)).fetchone()['n']; avail=c.execute("SELECT COUNT(*) n FROM drivers WHERE vehicle_type=? AND status='Available'",(t,)).fetchone()['n']; c.close()
 ratios=[]
 for r in hist:
  b=baseline(t,r['distance_km'],r['duration_min'])
  if b: ratios.append(r['fare']/b)
 ratios.sort(); historical=ratios[len(ratios)//2] if ratios else 1
 supply=1.20 if avail==0 else (1.15 if active>avail*2 else (1.07 if active>avail else 1))
 peak=1.08 if datetime.now().hour in list(range(7,10))+list(range(17,21)) else 1
 factor=max(.8,min(1.35,historical*supply*peak)); value=round(base*factor,2)
 spread=max(50,value*(.055 if len(ratios)>=20 else .09)); confidence=min(95,70+len(ratios)//2)
 return {'predicted_fare':value,'low':round(value-spread,2),'high':round(value+spread,2),'confidence':confidence,'model':'Historical + demand/supply hybrid','available_drivers':avail,'active_requests':active}
