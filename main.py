from fastapi import FastAPI
from starlette.responses import FileResponse

app = FastAPI()


@app.get("/")
async def root():
    return FileResponse('./static/index.html')