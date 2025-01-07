from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from src.uid_gen import Snowflake
from src.short_url import encode_uid_62
import sqlite3
import logging

con = sqlite3.connect("url.db", check_same_thread=False)
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS url (long_url TEXT, short_url TEXT)")


class URLItem(BaseModel):
    long_url: str


app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = Snowflake.load_config("config.json")
uid_generator = Snowflake(**config)

url_cache = {}


@app.post("/shorten")
def shorten_url(item: URLItem) -> dict[str, str]:
    """
    Shortens a given long URL.

    Args:
        item (URLItem): An object containing the long URL to be shortened.

    Returns:
        dict: A dictionary containing the shortened URL.
    """
    long_url = item.long_url
    db_short_url = cur.execute(
        "SELECT short_url FROM url WHERE long_url = ?", (long_url,)
    ).fetchone()
    if db_short_url:
        url_cache[db_short_url[0]] = long_url
        return {"short_url": db_short_url[0]}

    uid = uid_generator.generate_id()
    encoded_uid = encode_uid_62(uid)

    cur.execute("INSERT INTO url VALUES (?, ?)", (long_url, encoded_uid))
    con.commit()
    url_cache[encoded_uid] = long_url

    return {"short_url": encoded_uid}


@app.get("/{short_url}")
def redirect_url(short_url: str) -> RedirectResponse:
    """
    Redirects to the long URL corresponding to the given short URL.

    Args:
        short_url (str): The short URL to be redirected.

    Returns:
        RedirectResponse: A response object that redirects to the long URL.

    Raises:
        HTTPException: If the short URL does not exist in the mapping.
    """
    cache_long_url = url_cache.get(short_url)
    if cache_long_url:
        logger.info("Cache hit")
        return RedirectResponse(url=cache_long_url)

    db_long_url = cur.execute(
        "SELECT long_url FROM url WHERE short_url = ?", (short_url,)
    ).fetchone()
    if db_long_url:
        url_cache[short_url] = db_long_url[0]
        return RedirectResponse(url=db_long_url[0])

    raise HTTPException(status_code=404, detail="URL not found")
