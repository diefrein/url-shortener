import logging
from database.database import run_migrations
from fastapi import FastAPI
from api.routes.urls import router as url_router
import uvicorn, os

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