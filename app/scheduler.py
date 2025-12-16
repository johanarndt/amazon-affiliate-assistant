from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from .config import DEFAULT_MARKETS, POST_HOURS
from .db import SessionLocal
from .models import ScheduledPost, SalesPage, Product
from .services import get_social

scheduler = BackgroundScheduler()

def send_due_posts():
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        due = db.query(ScheduledPost).filter(ScheduledPost.sent == False, ScheduledPost.scheduled_for <= now).all()
        poster = get_social()
        for job in due:
            page = db.query(SalesPage).filter_by(id=job.sales_page_id).first()
            product = db.query(Product).filter_by(id=page.product_id).first() if page else None
            if not page or not product:
                job.sent = True
                job.result = "missing page/product"
                db.add(job); db.commit()
                continue
            link = page.affiliate_link or ""
            message = f"{job.content} {link}"
            res = poster.post(job.platform, job.market, job.language, message, link)
            job.sent = True
            job.result = res
            db.add(job); db.commit()
    finally:
        db.close()

def start_scheduler():
    # Run check every minute
    scheduler.add_job(send_due_posts, "interval", minutes=1, id="send_due_posts")
    scheduler.start()
