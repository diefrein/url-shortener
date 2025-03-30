import logging, uvicorn, os
from database.database import run_migrations
from fastapi import FastAPI
from api.routes.urls import router as url_router
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.scheduled_task import remove_expired_urls

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = FastAPI(
   title='url-shortener'
)
app.include_router(url_router, prefix='/api/v1')

def init_db():
   run_migrations()
    
if __name__ == "__main__":
   init_db()
   port = int(os.getenv('BACKEND_PORT'))
   log.info("Starting web-server with port = [%s]", port)
   uvicorn.run(app, host="0.0.0.0", port=port)
   
   scheduler = BackgroundScheduler()
   scheduler.add_job(remove_expired_urls, 'interval', seconds=30)
   scheduler.start()