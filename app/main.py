import time
import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f'Request: {request.method} {request.url.path}, Process Time: {process_time:.4f} seconds')
    return response


@app.get("/")
def root():
    """Serve the index.html file."""
    return FileResponse('./static/index.html')