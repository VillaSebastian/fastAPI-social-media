import time
import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.database import set_up_database
from app.routers import posts, users, login, views

# Create and configure logger
LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename="./database.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT)
logger = logging.getLogger()


set_up_database()


app = FastAPI()
app.title = "Social Media API"
app.version = "1.0"
app.include_router(login.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(views.router)

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