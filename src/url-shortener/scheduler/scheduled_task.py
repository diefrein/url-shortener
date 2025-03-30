import logging
from sqlalchemy.orm import sessionmaker
from database.database import *

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def remove_expired_urls():
    log.info("Started scheduled task (remove_expired_urls)")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    remove_expired_urls(session=session)
    log.info("Finished scheduled task (remove_expired_urls)")
    