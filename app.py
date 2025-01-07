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
