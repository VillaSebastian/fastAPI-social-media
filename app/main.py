import time
import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import set_up_database
from app.routers import posts, users, login

# Create and configure logger
LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename="./database.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT)
logger = logging.getLogger()


set_up_database()


app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(login.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

ignore_paths = ("/static/styles.css", "/static/scripts.js", "/favicon.ico")
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    if request.url.path not in ignore_paths:
        logging.info(f'Request: {request.method} {request.url.path}, Process Time: {process_time:.4f} seconds')
    return response

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the home.html template."""
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    """Serve the register.html template."""
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    """Serve the login.html template."""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/view/posts", response_class=HTMLResponse)
async def posts(request: Request):
    """Serve the posts.html template."""
    return templates.TemplateResponse("posts.html", {"request": request})