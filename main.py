import logging
from typing import Optional

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from core.db import init_db, get_user, create_user
from core.security import hash_password, verify_password
from utils import get_random_books

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
