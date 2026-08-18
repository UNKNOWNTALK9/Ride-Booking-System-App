import math
import customtkinter as ctk
from tkinter import messagebox
from database.database import init_db,connect
from services.auth_service import login,register
from services.booking_service import create_booking,list_user_rides,complete_ride
from services.ai_prediction_service import predict
from location.location_service import search_locations
try:
    from tkintermapview import TkinterMapView
    MAP_OK=True
except Exception:
    MAP_OK=False
ctk.set_appearance_mode('dark'); ctk.set_default_color_theme('green')
BG='#07111F'; PANEL='#0D1B2A'; CARD='#12263A'; TEXT='#F5F7FA'; MUTED='#9FB0C0'; GREEN='#16A085'; GOLD='#D9B44A'
class PakistanRideApp(ctk.CTk):
    def __init__(self):
        super().__init__(); init_db(); self.title('Pakistan Ride v3.0 — Ride Anywhere. Anytime.'); self.geometry('1400x860'); self.minsize(1050,680); self.configure(fg_color=BG); self.user=None; self.content=None; self.show_login()
    def clear(self):
        for w in self.winfo_children(): w.destroy()
    def page_title(self,t,s=''):
        for w in self.content.winfo_children(): w.destroy()
        ctk.CTkLabel(self.content,text=t,font=('Segoe UI',30,'bold'),text_color=TEXT).pack(anchor='w',padx=34,pady=(28,2))
        if s: ctk.CTkLabel(self.content,text=s,font=('Segoe UI',14),text_color=MUTED).pack(anchor='w',padx=34,pady=(0,20))
    def show_login(self):
        self.clear(); self.title('Pakistan Ride — Sign In')
        outer=ctk.CTkFrame(self,fg_color=BG,corner_radius=0); outer.pack(fill='both',expand=True)
        box=ctk.CTkFrame(outer,width=520,height=620,fg_color=CARD,corner_radius=25); box.place(relx=.5,rely=.5,anchor='center'); box.pack_propagate(False)
        ctk.CTkLabel(box,text='🇵🇰 Pakistan Ride',font=('Segoe UI',34,'bold')).pack(pady=(55,5)); ctk.CTkLabel(box,text='Ride Anywhere. Anytime.',font=('Segoe UI',17),text_color=GOLD).pack(pady=(0,30))
        self.login_user=ctk.CTkEntry(box,width=370,height=48,placeholder_text='Username'); self.login_user.pack(pady=8)
        self.login_pass=ctk.CTkEntry(box,width=370,height=48,placeholder_text='Password',show='•'); self.login_pass.pack(pady=8)
        ctk.CTkButton(box,text='Sign In',width=370,height=48,fg_color=GREEN,command=self.do_login).pack(pady=20)
        ctk.CTkButton(box,text='Create Passenger Account',width=370,height=42,fg_color='transparent',border_width=1,command=self.register_dialog).pack()
        ctk.CTkLabel(box,text='Demo: passenger/passenger123   admin/admin123   driver/driver123',text_color=MUTED).pack(pady=25)
    def do_login(self):
        self.user=login(self.login_user.get(),self.login_pass.get())
        if not self.user: messagebox.showerror('Login failed','Invalid username or password.'); return
        self.dashboard()
    def register_dialog(self):
        w=ctk.CTkToplevel(self); w.title('Create Passenger Account'); w.geometry('450x500'); w.grab_set(); es=[]
        for lab in ['Full name','Username','Password','Phone']:
            ctk.CTkLabel(w,text=lab).pack(anchor='w',padx=35,pady=(12,2)); e=ctk.CTkEntry(w,width=360,show='•' if lab=='Password' else ''); e.pack(padx=35); es.append(e)
        def save():
            try: register(*(e.get() for e in es)); messagebox.showinfo('Success','Account created.'); w.destroy()
            except ValueError as ex: messagebox.showerror('Registration',str(ex))
        ctk.CTkButton(w,text='Create Account',command=save).pack(pady=28)
    def dashboard(self):
        self.clear(); side=ctk.CTkFrame(self,width=245,corner_radius=0); side.pack(side='left',fill='y'); side.pack_propagate(False)
        ctk.CTkLabel(side,text='🇵🇰 Pakistan Ride',font=('Segoe UI',22,'bold')).pack(pady=25); ctk.CTkLabel(side,text=self.user['name'],text_color=MUTED).pack(pady=(0,18))
        nav=[('🏠 Home',self.home),('🗺️ Smart Map',self.map_booking),('🧾 History',self.history),('❤️ Favorites',self.favorites),('💳 Payments',self.payments),('🔔 Alerts',self.alerts),('⚙ Settings',self.settings)]
        if self.user['role']=='Admin': nav.insert(1,('📊 Admin AI',self.admin))
        if self.user['role']=='Driver': nav.insert(1,('🚘 Driver',self.driver))
        for n,cmd in nav: ctk.CTkButton(side,text=n,anchor='w',fg_color='transparent',height=43,command=cmd).pack(fill='x',padx=14,pady=3)
        ctk.CTkButton(side,text='Logout',fg_color='#7f1d1d',command=self.show_login).pack(side='bottom',fill='x',padx=14,pady=20)
        self.content=ctk.CTkFrame(self,corner_radius=0); self.content.pack(side='left',fill='both',expand=True); self.home()
    def home(self):
        self.page_title('Good Morning!','Smart booking: select your route directly from the Pakistan map.')
        ctk.CTkLabel(self.content,text='🗺️ Click pickup → click destination → AI predicts distance, ETA and fare.',font=('Segoe UI',20,'bold')).pack(pady=50)
        ctk.CTkButton(self.content,text='Open Smart Map Booking',width=330,height=55,command=self.map_booking).pack()
        ctk.CTkLabel(self.content,text='🚗 Car   🏍️ Bike   🚐 Van   🚌 Bus   🛺 Rickshaw',font=('Segoe UI',18),text_color=GOLD).pack(pady=35)
    def map_booking(self):
        self.page_title('Smart Map Booking','No need to type pickup or destination. Click the map.')
        top=ctk.CTkFrame(self.content,fg_color='transparent'); top.pack(fill='x',padx=30)
        self.picktxt=ctk.CTkLabel(top,text='📍 Pickup: Not selected',font=('Segoe UI',14,'bold')); self.picktxt.pack(side='left',padx=8)
        self.destxt=ctk.CTkLabel(top,text='🏁 Destination: Not selected',font=('Segoe UI',14,'bold')); self.destxt.pack(side='left',padx=30)
        self.ride=ctk.StringVar(value='Car')
        for r in ['Car','Bike','Van','Bus','Rickshaw']: ctk.CTkRadioButton(top,text=r,variable=self.ride,value=r,command=self.update_prediction).pack(side='right',padx=5)
        body=ctk.CTkFrame(self.content,corner_radius=18); body.pack(fill='both',expand=True,padx=30,pady=12); body.grid_columnconfigure(0,weight=3); body.grid_columnconfigure(1,weight=1); body.grid_rowconfigure(0,weight=1)
        if MAP_OK:
            self.map=TkinterMapView(body,corner_radius=15); self.map.grid(row=0,column=0,sticky='nsew',padx=10,pady=10); self.map.set_position(30.3753,69.3451); self.map.set_zoom(5); self.map.add_left_click_map_command(self.map_click)
        else:
            p=ctk.CTkFrame(body); p.grid(row=0,column=0,sticky='nsew',padx=10,pady=10); ctk.CTkLabel(p,text='Map component unavailable.\nRun:\npip install -r requirements.txt',font=('Segoe UI',18),justify='center').place(relx=.5,rely=.5,anchor='center')
            self.map=None
        panel=ctk.CTkFrame(body,corner_radius=15); panel.grid(row=0,column=1,sticky='nsew',padx=(5,10),pady=10)
        ctk.CTkLabel(panel,text='Location Search',font=('Segoe UI',18,'bold')).pack(anchor='w',padx=18,pady=(18,7)); self.search=ctk.CTkEntry(panel,placeholder_text='Clifton / Skardu / DHA Lahore'); self.search.pack(fill='x',padx=18); ctk.CTkButton(panel,text='Search',command=self.location_search).pack(fill='x',padx=18,pady=7)
        self.results=ctk.CTkScrollableFrame(panel,height=180); self.results.pack(fill='both',expand=True,padx=18,pady=7)
        self.distance=ctk.CTkLabel(panel,text='Distance: —',font=('Segoe UI',16,'bold')); self.distance.pack(anchor='w',padx=18,pady=(8,2)); self.eta=ctk.CTkLabel(panel,text='ETA: —'); self.eta.pack(anchor='w',padx=18)
        self.ai=ctk.CTkLabel(panel,text='🤖 AI Fare: —',font=('Segoe UI',20,'bold')); self.ai.pack(anchor='w',padx=18,pady=(18,2)); self.airange=ctk.CTkLabel(panel,text='Range: —'); self.airange.pack(anchor='w',padx=18); self.conf=ctk.CTkLabel(panel,text='Confidence: —'); self.conf.pack(anchor='w',padx=18)
        ctk.CTkButton(panel,text='Reset',command=self.reset_map).pack(fill='x',padx=18,pady=8); ctk.CTkButton(panel,text='Confirm AI Ride',height=48,command=self.confirm_map).pack(fill='x',padx=18,pady=(4,18))
        self.stage='pickup'; self.pickup=None; self.destination=None; self.pm=None; self.dm=None
    def map_click(self,coords):
        lat,lon=coords; label=f'Map point ({lat:.5f}, {lon:.5f})'
        if self.stage=='pickup':
            self.pickup=(lat,lon,label); self.picktxt.configure(text='📍 Pickup: '+label); self.pm=self.map.set_marker(lat,lon,text='Pickup'); self.stage='destination'
        else:
            self.destination=(lat,lon,label); self.destxt.configure(text='🏁 Destination: '+label); self.dm=self.map.set_marker(lat,lon,text='Destination'); self.update_prediction()
    def location_search(self):
        for w in self.results.winfo_children(): w.destroy()
        rows=search_locations(self.search.get())
        for r in rows[:15]: ctk.CTkButton(self.results,text=f"{r['name']} • {r['level']}",anchor='w',command=lambda x=r:self.select_location(x)).pack(fill='x',pady=2)
        if not rows: ctk.CTkLabel(self.results,text='No starter location found.').pack(pady=8)
    def select_location(self,row):
        if not self.map: return
        try:
            m=self.map.set_address(row['name']+', Pakistan',marker=True); self.map.set_zoom(13); lat,lon=m.position
            if self.stage=='pickup': self.pickup=(lat,lon,row['name']); self.picktxt.configure(text='📍 Pickup: '+row['name']); self.pm=m; self.stage='destination'
            else: self.destination=(lat,lon,row['name']); self.destxt.configure(text='🏁 Destination: '+row['name']); self.dm=m; self.update_prediction()
        except Exception as e: messagebox.showerror('Map search',str(e))
    def update_prediction(self):
        if not self.pickup or not self.destination: return
        lat1,lon1,_=self.pickup; lat2,lon2,_=self.destination; R=6371; p1=math.radians(lat1); p2=math.radians(lat2); dp=math.radians(lat2-lat1); dl=math.radians(lon2-lon1); a=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2; straight=2*R*math.asin(math.sqrt(a)); km=max(.2,straight*1.22); speed={'Car':34,'Bike':32,'Van':30,'Bus':28,'Rickshaw':25}[self.ride.get()]; mins=max(3,km/speed*60); self.km=km; self.mins=mins; p=predict(self.ride.get(),km,mins); self.distance.configure(text=f'Distance: {km:.1f} km'); self.eta.configure(text=f'ETA: {mins:.0f} min'); self.ai.configure(text=f"🤖 AI Fare: PKR {p['predicted_fare']:,.0f}"); self.airange.configure(text=f"Range: PKR {p['low']:,.0f} – {p['high']:,.0f}"); self.conf.configure(text=f"Confidence: {p['confidence']}% • {p['model']}")
    def reset_map(self):
        self.stage='pickup'; self.pickup=self.destination=None
        if getattr(self,'pm',None): self.pm.delete()
        if getattr(self,'dm',None): self.dm.delete()
        self.picktxt.configure(text='📍 Pickup: Not selected'); self.destxt.configure(text='🏁 Destination: Not selected'); self.distance.configure(text='Distance: —'); self.eta.configure(text='ETA: —'); self.ai.configure(text='🤖 AI Fare: —'); self.airange.configure(text='Range: —'); self.conf.configure(text='Confidence: —')
    def confirm_map(self):
        if not self.pickup or not self.destination: messagebox.showwarning('Route','Select pickup and destination.'); return
        p=predict(self.ride.get(),self.km,self.mins)
        try:
            rid,fare,d=create_booking(self.user['id'],self.ride.get(),self.pickup[2],self.destination[2],self.km,self.mins); msg=f'Ride #{rid}\nAI fare: PKR {p["predicted_fare"]:,.0f}\nRange: PKR {p["low"]:,.0f} – {p["high"]:,.0f}\nSaved fare: PKR {fare:,.0f}';
            if d: msg+=f'\n\nDriver: {d["name"]}\n{d["vehicle_model"]} • {d["vehicle_number"]}'
            messagebox.showinfo('Ride Confirmed',msg); self.history()
        except Exception as e: messagebox.showerror('Booking',str(e))
    def history(self):
        self.page_title('Ride History','Your bookings'); rows=list_user_rides(self.user['id'])
        if not rows: ctk.CTkLabel(self.content,text='No rides yet.').pack(pady=50); return
        for r in rows[:20]:
            card=ctk.CTkFrame(self.content,corner_radius=14); card.pack(fill='x',padx=35,pady=6); ctk.CTkLabel(card,text=f"#{r['id']}  {r['ride_type']} • {r['status']} • PKR {r['fare']:,.0f}\n{r['pickup']} → {r['destination']}",justify='left').pack(side='left',padx=18,pady=12)
            if r['status'] not in ('Ride Completed','Cancelled'): ctk.CTkButton(card,text='Complete Demo Ride',command=lambda i=r['id']:(complete_ride(i),self.history())).pack(side='right',padx=15)
    def favorites(self): self.page_title('Saved Places'); ctk.CTkLabel(self.content,text='Saved-place UI is ready for extension.').pack(pady=50)
    def payments(self): self.page_title('Payments'); ctk.CTkLabel(self.content,text='Local demo payment records. No real payment processing.').pack(pady=50)
    def alerts(self): self.page_title('Notifications'); ctk.CTkLabel(self.content,text='No new notifications.').pack(pady=50)
    def settings(self):
        self.page_title('Settings'); ctk.CTkLabel(self.content,text='Appearance').pack(anchor='w',padx=40,pady=10); ctk.CTkOptionMenu(self.content,values=['Dark','Light','System'],command=ctk.set_appearance_mode).pack(anchor='w',padx=40); ctk.CTkLabel(self.content,text='Language').pack(anchor='w',padx=40,pady=(20,5)); ctk.CTkOptionMenu(self.content,values=['English','Urdu']).pack(anchor='w',padx=40)
    def driver(self): self.page_title('Driver Dashboard','Demo mode'); ctk.CTkSwitch(self.content,text='Online / Available').pack(anchor='w',padx=40,pady=20)
    def admin(self):
        self.page_title('Admin + AI','Prediction and operations'); c=connect(); vals=[('Users','SELECT COUNT(*) FROM users'),('Drivers','SELECT COUNT(*) FROM drivers'),('Rides','SELECT COUNT(*) FROM rides'),('Completed',"SELECT COUNT(*) FROM rides WHERE status='Ride Completed'")]; row=ctk.CTkFrame(self.content,fg_color='transparent'); row.pack(fill='x',padx=30)
        for i,(n,q) in enumerate(vals): row.grid_columnconfigure(i,weight=1); x=ctk.CTkFrame(row,corner_radius=16); x.grid(row=0,column=i,sticky='nsew',padx=5); ctk.CTkLabel(x,text=n).pack(pady=(18,3)); ctk.CTkLabel(x,text=str(c.execute(q).fetchone()[0]),font=('Segoe UI',24,'bold')).pack(pady=(0,18))
        c.close(); ctk.CTkLabel(self.content,text='AI uses configured fare rules and learns from completed local demo rides when enough history exists.',font=('Segoe UI',15)).pack(pady=35)
if __name__=='__main__': PakistanRideApp().mainloop()
