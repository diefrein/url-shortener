import logging
from database.database import create_user, engine
from database.models import UserCreate
from sqlalchemy.orm import sessionmaker
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
   log.info("Creating initial data")
   Session = sessionmaker(bind=engine)
   session = Session()
   
   create_user(session=session, user_create=UserCreate(name="test user"))
   log.info("Creating initial data")
    
if __name__ == "__main__":
   init_db()
   port = int(os.getenv('BACKEND_PORT'))
   log.info("Starting web-server with port = [%s]", port)
   uvicorn.run(app, host="0.0.0.0", port=port)