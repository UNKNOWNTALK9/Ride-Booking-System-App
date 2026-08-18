from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
def generate_receipt(payment_id,ride,amount,method):
 p=Path(__file__).resolve().parent/f'receipt_{payment_id}.pdf';c=canvas.Canvas(str(p),pagesize=A4);c.setFont('Helvetica-Bold',22);c.drawString(60,780,'Pakistan Ride');c.setFont('Helvetica',11);y=735
 for s in [f'Payment ID: {payment_id}',f'Ride ID: {ride["id"]}',f'Ride: {ride["ride_type"]}',f'Pickup: {ride["pickup"]}',f'Destination: {ride["destination"]}',f'Amount: PKR {amount:,.2f}',f'Method: {method}','Status: Paid','DEMO RECEIPT']:
  c.drawString(60,y,s);y-=28
 c.save();return str(p)
