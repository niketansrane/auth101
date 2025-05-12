import jwt
import logging
import requests

from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from oauthlib.oauth2 import WebApplicationClient

from core.db import init_db, get_user, create_user
from core.security import hash_password, verify_password
from utils import get_random_books
from config import Environment

# Setup
logging.basicConfig(level=logging.INFO)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

HOMEPAGE_HTML = "home_page.html"
BORROWED_BOOKS_HTML = "borrowed_books.html"


# Initialize the DB
init_db()


# Endpoints
@app.get("/", response_class=HTMLResponse)
def home(request: Request, message: Optional[str] = None):
    return templates.TemplateResponse(HOMEPAGE_HTML, {"request": request, "message": message})

@app.get("/microsoftlogin")
def read_login():
    web_client = WebApplicationClient(Environment.CLIENT_ID)
    request_uri = web_client.prepare_request_uri(
        uri=Environment.AUTHORIZE_URL, redirect_uri=Environment.REDIRECT_URI, scope=Environment.SCOPE, state=Environment.STATE
    )
    print(f"Request URI: {request_uri}")
    return RedirectResponse(url=request_uri, status_code=302)


@app.get("/callback")
def callback(code: str):
    web_client = WebApplicationClient(Environment.CLIENT_ID)
    request_body = web_client.prepare_request_body(code=code, redirect_uri=Environment.REDIRECT_URI)
    response = requests.post(Environment.TOKEN_URL, data=request_body)
    web_client.parse_request_body_response(response.text)
    token = web_client.access_token
    # decode token
    decoded = jwt.decode(token, options={"verify_signature": False})
    username = decoded.get("unique_name")
    username = decoded.get("sub") if username is None else username
    
    response = RedirectResponse(url="/books", status_code=302)
    response.set_cookie(key="username", value=username)
    return response


@app.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...)):
    if get_user(username):
        return templates.TemplateResponse(
            HOMEPAGE_HTML,
            {"request": request, "message": "Username already exists. Try another!", "username": username}
        )
    hashed_pw = hash_password(password)
    create_user(username, hashed_pw)

    return templates.TemplateResponse(
        HOMEPAGE_HTML,
        {"request": request, "message": "User registered successfully! Please log in.", "username": username}
    )


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = get_user(username)
    if not user:
        return templates.TemplateResponse(
            HOMEPAGE_HTML,
            {"request": request, "message": "User does not exist.", "username": username}
        )

    if not verify_password(password, user["hashed_password"]):
        return templates.TemplateResponse(
            HOMEPAGE_HTML,
            {"request": request, "message": "Invalid password.", "username": username}
        )

    response = RedirectResponse(url="/books", status_code=302)
    response.set_cookie(key="username", value=username)
    return response


@app.get("/books", response_class=HTMLResponse)
def books(request: Request):
    username = request.cookies.get("username")
    if not username:
        return RedirectResponse(url="/", status_code=302)

    books = get_random_books()
    return templates.TemplateResponse(
        BORROWED_BOOKS_HTML,
        {"request": request, "username": username, "books": books}
    )
