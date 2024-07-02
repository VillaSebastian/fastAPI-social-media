from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(
    tags=['Views']
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the home.html template."""
    return templates.TemplateResponse(request, "home.html")

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    """Serve the register.html template."""
    return templates.TemplateResponse(request, "register.html")

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    """Serve the login.html template."""
    return templates.TemplateResponse(request, "login.html")

@router.get("/view/posts", response_class=HTMLResponse)
async def posts(request: Request):
    """Serve the posts.html template."""
    return templates.TemplateResponse(request, "posts.html")

@router.get("/view/posts/{id}", response_class=HTMLResponse)
async def post_id(request: Request):
    """Serve the posts_id.html template."""
    return templates.TemplateResponse(request, "post_detail.html")