from pathlib import Path
import sqlite3
ROOT=Path(__file__).resolve().parent.parent
DB_PATH=ROOT/'database'/'pakistan_ride.db'
def connect():
    DB_PATH.parent.mkdir(exist_ok=True)
    c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c
def init_db():
    c=connect(); c.executescript('''
CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,username TEXT UNIQUE,password_hash TEXT,role TEXT,name TEXT,phone TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS drivers(id INTEGER PRIMARY KEY,user_id INTEGER,name TEXT,phone TEXT,vehicle_type TEXT,vehicle_model TEXT,vehicle_number TEXT,capacity INTEGER,rating REAL DEFAULT 5,total_rides INTEGER DEFAULT 0,status TEXT DEFAULT 'Available',current_location TEXT);
CREATE TABLE IF NOT EXISTS locations(id INTEGER PRIMARY KEY,parent_id INTEGER,level TEXT,name TEXT,name_ur TEXT,normalized TEXT,province TEXT,division TEXT,district TEXT,tehsil TEXT,city TEXT,category TEXT);
CREATE INDEX IF NOT EXISTS idx_locations_normalized ON locations(normalized);
CREATE TABLE IF NOT EXISTS ride_types(id INTEGER PRIMARY KEY,name TEXT UNIQUE,description TEXT,base_fare REAL,per_km REAL,per_minute REAL,capacity INTEGER);
CREATE TABLE IF NOT EXISTS rides(id INTEGER PRIMARY KEY,user_id INTEGER,driver_id INTEGER,ride_type TEXT,pickup TEXT,destination TEXT,distance_km REAL,duration_min REAL,fare REAL,status TEXT,requested_at TEXT,completed_at TEXT);
CREATE TABLE IF NOT EXISTS payments(id INTEGER PRIMARY KEY,ride_id INTEGER,user_id INTEGER,amount REAL,method TEXT,status TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS ratings(id INTEGER PRIMARY KEY,ride_id INTEGER,driver_id INTEGER,passenger_id INTEGER,rating INTEGER,review TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS saved_places(id INTEGER PRIMARY KEY,user_id INTEGER,label TEXT,location TEXT);
CREATE TABLE IF NOT EXISTS notifications(id INTEGER PRIMARY KEY,user_id INTEGER,title TEXT,body TEXT,created_at TEXT,read INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS complaints(id INTEGER PRIMARY KEY,user_id INTEGER,ride_id INTEGER,subject TEXT,message TEXT,status TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT);
'''); seed(c); c.close()
def seed(c):
    from services.auth_service import hash_password
    from datetime import datetime
    now=datetime.now().isoformat(timespec='seconds')
    for u,p,r,n in [('admin','admin123','Admin','System Admin'),('driver','driver123','Driver','Ali Khan'),('passenger','passenger123','Passenger','Hammad')]:
        c.execute('INSERT OR IGNORE INTO users(username,password_hash,role,name,phone,created_at) VALUES(?,?,?,?,?,?)',(u,hash_password(p),r,n,'',now))
    for x in [('Car','Comfortable',180,55,4,4),('Bike','Economical',80,28,2,1),('Van','Family',280,75,5,7),('Bus','Group',500,95,8,30),('Rickshaw','Local',100,35,3,3)]: c.execute('INSERT OR IGNORE INTO ride_types(name,description,base_fare,per_km,per_minute,capacity) VALUES(?,?,?,?,?,?)',x)
    du=c.execute("SELECT id FROM users WHERE username='driver'").fetchone()[0]
    if not c.execute('SELECT 1 FROM drivers LIMIT 1').fetchone():
        for n,t,m,v,cap,r in [('Ali Khan','Car','Toyota Corolla','CAR-123',4,4.8),('Ahmed','Bike','Honda CD 70','BIKE-456',1,4.7),('Usman','Van','Suzuki Bolan','VAN-789',7,4.6),('Bilal','Rickshaw','Qingqi Rickshaw','RKS-222',3,4.5),('Sajid','Bus','Daewoo Bus','BUS-555',30,4.7)]: c.execute("INSERT INTO drivers(user_id,name,vehicle_type,vehicle_model,vehicle_number,capacity,rating,status,current_location) VALUES(?,?,?,?,?,?,?,?,?)",(du if n=='Ali Khan' else None,n,t,m,v,cap,r,'Available',n+' Demo Location'))
    c.commit()
