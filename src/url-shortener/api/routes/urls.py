from fastapi import APIRouter, Query
from database.models import Url, UrlCreate, UrlStatistics
from database.database import *
from sqlalchemy.orm import sessionmaker
from fastapi.responses import RedirectResponse, PlainTextResponse
from urlgenerator.generator import generate_short_url

router = APIRouter(prefix="/links", tags=["urls"])

@router.post("/shorten", response_model=None)
def create_url_endpoint(url_create: UrlCreate) -> Url:
    """
    Create url
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    
    short_url = url_create.custom_alias
    if url_create.custom_alias is None:
        short_url = generate_short_url(full_url=url_create.full_url)
    else:
        short_url = url_create.custom_alias
    url = Url(
        full_url = url_create.full_url,
        short_url = short_url,
        user_id = url_create.user_id,
        created_at = datetime.now(),
        expires_at = url_create.expires_at
    )
    
    return create_url(session=session, url=url)

@router.get("/search", response_model=None)
def get_url_endpoint(ids: list = Query(None), short_url: str = Query(None), origin_url: str = Query(None)) -> Url:
    """
    Get urls by filters
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    return get_urls(session=session, ids=ids, short_url=short_url, full_url=origin_url)

@router.get("/{short_url}", response_model=None)
def get_url_endpoint(short_url: str) -> Url:
    """
    Get url by short url and redirect user
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    
    url = _get_single_url(session=session, short_url=short_url)
    update_url_use_count(session=session, url_id=url.id)
    return RedirectResponse(url=url.full_url, status_code=307)

@router.delete("/{short_url}", response_model=None)
def delete_short_url_endpoint(short_url: str):
    """
    Delete short url
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        url = _get_single_url(session=session, short_url=short_url)
        delete_url(session=session, url_id=url.id)
    except Exception as e:
        return PlainTextResponse(e)

@router.put("/{short_url}", response_model=None)
def delete_short_url_endpoint(short_url: str, new_short_url: str) -> Url:
    """
    Update short url
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        url = _get_single_url(session=session, short_url=short_url)
        url.short_url = new_short_url
        return update_url(session=session, url=url)
    except Exception as e:
        return PlainTextResponse(e)

@router.get("/{short_url}/stats", response_model=None)
def get_url_stats_endpoint(short_url: str) -> UrlStatistics:
    """
    Get url statistics 
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        url = _get_single_url(session=session, short_url=short_url)
        return UrlStatistics(
                full_url=url.full_url,
                times_used=url.times_used,
                created_at=url.created_at,
                latest_used_at=url.latest_used_at,
                expires_at=url.expires_at
            )
    except Exception as e:
        return PlainTextResponse(e)
    
def _get_single_url(session: Session, short_url: str) -> Url:
    urls = get_urls(session=session, short_url=short_url)
    size = len(urls)
    
    if (size < 1):
        log.error(f"No url found for short_url = {short_url}")
        raise RuntimeError("No url found for given short one")
    elif (size == 1):
        return urls[0]
    else:
        log.error(f"More then one url found for short_url = {short_url}")
        raise RuntimeError("More then one url found")