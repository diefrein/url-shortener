import logging
from database.database import create_user, engine
from database.models import UserCreate
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def init_db():
   log.info("Creating initial data")
   Session = sessionmaker(bind=engine)

   session = Session()
   create_user(session=session, user_create=UserCreate("test user"))
   log.info("Creating initial data")
    
if __name__ == "__main__":
   init_db()