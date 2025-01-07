from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from src.uid_gen import Snowflake
from src.short_url import encode_uid_62


class URLItem(BaseModel):
    long_url: str


app = FastAPI()
config = Snowflake.load_config("config.json")
uid_generator = Snowflake(**config)
long_to_short_url_map = {}
short_to_long_url_map = {}


@app.post("/shorten")
def shorten_url(item: URLItem):
    """
    Shortens a given long URL.

    Args:
        item (URLItem): An object containing the long URL to be shortened.

    Returns:
        dict: A dictionary containing the shortened URL.
    """
    long_url = item.long_url
    short_url = long_to_short_url_map.get(long_url)
    if short_url:
        return {"short_url_retrieved": short_url}

    uid = uid_generator.generate_id()
    encoded_uid = encode_uid_62(uid)

    long_to_short_url_map[long_url] = encoded_uid
    short_to_long_url_map[encoded_uid] = long_url

    return {"short_url": encoded_uid}
