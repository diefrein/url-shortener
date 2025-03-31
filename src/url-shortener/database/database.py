from sqlalchemy import create_engine, text
from database.models import *
from database.config import DATABASE_URL
from sqlalchemy.orm import Session, sessionmaker
import logging, uuid
from urlgenerator.generator import generate_short_url
from datetime import datetime
from caching.custom_cache import cache_query, invalidate_cache

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL)

create_users_native_sql =  """
            create table if not exists users(
                id uuid primary key default gen_random_uuid(), 
                name varchar not null)
            """

create_urls_native_sql = """
            create table if not exists urls(
                id uuid primary key default gen_random_uuid(), 
                full_url varchar not null, 
                short_url varchar not null, 
                user_id uuid not null)
            """

alter_urls_native_sql = """
            alter table urls add column if not exists created_at timestamp not null default now();
            alter table urls add column if not exists latest_used_at timestamp;
            alter table urls add column if not exists times_used integer not null default 0;
            alter table urls add column if not exists expires_at timestamp;
            """

def run_migrations():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        session.execute(text(create_users_native_sql))
        log.info("Created users table")
        
        session.execute(text(create_urls_native_sql))
        log.info("Created urls table")
        
        session.execute(text(alter_urls_native_sql))
        log.info("Altered urls table")
        
        session.commit()
    except Exception as e:
        log.error(f"Exception while applying migrations", e)
        session.rollback()  

def create_user(*, session: Session, user_create: UserCreate) -> User:
    try:
        user = User(
            name = user_create.name
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        log.info(f"User {user} was created")
        return user
    except Exception as e:
        log.error(f"Exception while creating user", e)
        session.rollback() 
        
def delete_user(*, session: Session, user_id: uuid):
    try:
        user = session.query(User).filter_by(id=user_id).first()
        
        if user:
            session.delete(user)
            session.commit()
            log.info(f"User with id = {user_id} was deleted")
        else:
            log.warning(f"User with id = {user_id} not found")
    except Exception as e:
        log.error(f"Exception while deleting user with id = {user_id}", e)
        session.rollback()
        
@invalidate_cache(pattern='get_urls*')
def create_url(*, session: Session, url_create: UrlCreate) -> Url:
    try:
        short_url = generate_short_url(full_url=url_create.full_url)
        url = Url(
            full_url = url_create.full_url,
            short_url = short_url,
            user_id = url_create.user_id,
            created_at = datetime.now(),
            expires_at = url_create.expires_at
        )
        session.add(url)
        session.commit()
        session.refresh(url)
        log.info(f"Url {url} was created")
        return url
    except Exception as e:
        log.error(f"Exception while creating url", e)
        session.rollback() 
        
@invalidate_cache(pattern='get_urls*')
def create_url(*, session: Session, url: Url) -> Url:
    try:
        session.add(url)
        session.commit()
        session.refresh(url)
        log.info(f"Url {url} was created")
        return url
    except Exception as e:
        log.error(f"Exception while creating url", e)
        session.rollback() 
        
@invalidate_cache(pattern='get_urls*')
def delete_url(*, session: Session, url_id: uuid):
    try:
        url = session.query(Url).filter_by(id=url_id).first()
        
        if url:
            session.delete(url)
            session.commit()
            log.info(f"Url with id = {url_id} was deleted")
        else:
            log.warning(f"Url with id = {url_id} not found")
    except Exception as e:
        log.error(f"Exception while deleting url with id = {url_id}", e)
        session.rollback() 
        
@cache_query()
def get_urls(*, session: Session, ids: list = None, short_url: str = None, full_url: str = None) -> list:
    try:
        query = session.query(Url)
        if ids:
            query = query.filter(Url.id.in_(ids))
        if short_url:
            query = query.filter(Url.short_url == short_url)
        if full_url:
            query = query.filter(Url.full_url == full_url)
        return query.all()
    except Exception as e:
        log.error(f"Exception while getting urls", e)
        session.rollback()
        
@invalidate_cache(pattern='get_urls*')
def update_url_use_count(*, session: Session, url_id: uuid):
    try:
        session.execute(
            text(
                f"""
                update urls set times_used = times_used + 1, latest_used_at = now() where id = '{url_id}'
                """
            )
        )
        session.commit()
        log.info(f"Updated url use count for url with id = {url_id}")
    except Exception as e:
        log.error(f"Exception while updating url use count for url with id = {url_id}", e)
        session.rollback()
        
@invalidate_cache(pattern='get_urls*')
def update_url(*, session: Session, url: Url) -> Url:
    try:
        session.add(url)
        session.commit()
        session.refresh(url)    
        log.info(f"Updated url with id = {url.id}")
    except Exception as e:
        log.error(f"Exception while updating with id = {url.id}", e)
        session.rollback()
        
@invalidate_cache(pattern='get_urls*')
def remove_expired_urls(*, session: Session):
    try:
        session.execute(text(
            f"""
            delete from urls where expires_at is not null and now() >= expires_at
            """
        ))
        session.commit()
        log.info(f"Deleted expired urls")
    except Exception as e:
        log.error(f"Exception while deleting expired urls", e)
        session.rollback()