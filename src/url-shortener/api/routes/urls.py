from uuid import UUID
from fastapi import APIRouter, Query
from database.models import Url, UrlCreate
from database.database import delete_url, engine, get_urls
from sqlalchemy.orm import sessionmaker
from database.database import create_url
from fastapi.responses import RedirectResponse, PlainTextResponse

router = APIRouter(prefix="/urls", tags=["urls"])

@router.post("/shorten", response_model=None)
def create_url_endpoint(url_create: UrlCreate) -> Url:
    """
    Create url
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    return create_url(session=session, url_create=url_create)

@router.delete("/{id}", response_model=None)
def delete_url_endpoint(id: UUID) -> Url:
    """
    Delete url
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    return delete_url(session=session, url_id=id)

@router.get("/", response_model=None)
def get_url_endpoint(ids: list = Query(None), short_url: str = Query(None)) -> Url:
    """
    Get urls by filters
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    return get_urls(session=session, ids=ids, short_url=short_url)

@router.get("/{short_url}", response_model=None)
def get_url_endpoint(short_url: str) -> Url:
    """
    Get url by short url and redirect user
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    urls = get_urls(session=session, short_url=short_url)
    size = len(urls)
    if (size < 1):
        return PlainTextResponse(content="No url found for given short one", status_code=400)
    elif (size == 1):
        return RedirectResponse(url=urls[0].full_url, status_code=307)
    else:
        return PlainTextResponse(content="More then one url found, please use the original one", status_code=400)
