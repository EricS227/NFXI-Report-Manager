from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.models import get_db
from sqlmodel import Session

router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form("financeiro"),
    db: Session = Depends(get_db)
):
    UserService(db).create_user(username, password, role)
    return RedirectResponse("/login", status_code=302)

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        raise HTTPException(400, "Username e password são obrigatórios")
    
    service = AuthService(db)
    token = service.authenticate(username, password)

    if not token:
        raise HTTPException(401, "Credenciais inválidas")
    
    return JSONResponse({"token": token})