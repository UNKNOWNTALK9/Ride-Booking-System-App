from database.database import connect
def dashboard_stats():
 c=connect();q=lambda s:c.execute(s).fetchone()[0];x={'users':q('SELECT COUNT(*) FROM users'),'drivers':q('SELECT COUNT(*) FROM drivers'),'rides':q('SELECT COUNT(*) FROM rides'),'completed':q("SELECT COUNT(*) FROM rides WHERE status='Ride Completed'"),'cancelled':q("SELECT COUNT(*) FROM rides WHERE status='Cancelled'"),'revenue':q("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='Paid'")};c.close();return x
