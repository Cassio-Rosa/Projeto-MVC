from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.auth import hash_senha, verificar_senha, criar_token

# APIROUTER agrupa as rotas desse arquivo com o prefixo /auth
router = APIRouter(prefix="/auth", tags=["Autenticação"])

#Configura para renderizar os templates
templates = Jinja2Templates(directory="app/templates")


# Rota para tela de cadastro
@router.get("/cadastro")
def tela_cadastro(request: Request):
    return templates.TemplateResponse(
        request, "auth/cadastro.html",
        {"request": request})

# Tela Login
@router.get("/login")
def tela_login(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/login.html",
        {"request": request}
    )