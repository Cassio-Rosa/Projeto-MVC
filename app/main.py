from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.controllers import auth_controller

app = FastAPI(title="Sistema de MVC")

#Configurar o fastapi para servir os arquivos CSS, JS, IMG
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#Configura para renderizar os templates HTML
templates = Jinja2Templates(directory="app/templates")

#Inclui os routeres do controller
app.include_router(auth_controller.router)