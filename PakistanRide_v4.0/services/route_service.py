import math
def haversine(a,b,c,d):
 R=6371; p1=math.radians(a); p2=math.radians(c); dp=math.radians(c-a); dl=math.radians(d-b); x=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2; return 2*R*math.asin(math.sqrt(x))
def road_distance_km(a,b,c,d): return max(.2,haversine(a,b,c,d)*1.22)
def eta_minutes(km,t): return max(3,km/{'Car':34,'Bike':32,'Van':30,'Bus':28,'Rickshaw':25}.get(t,30)*60)
