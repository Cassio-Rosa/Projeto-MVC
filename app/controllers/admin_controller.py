from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario

from app.auth import hash_senha, get_admin


# APIROUTER agrupa as rotas desse arquivo com o prefixo /auth
router = APIRouter(prefix="/usuarios", tags=["Usuários"])

#Configura para renderizar os templates
templates = Jinja2Templates(directory="app/templates")


#Listar todos os usuarios
@router.get("/")
def listar_usuarios(
    request: Request,
    db: Session = Depends(get_db),
    admin = Depends(get_admin), # Bloqueia quem não é admin    
):
    #Pegar todos os usuarios do banco de dados
    usuarios = db.query(Usuario).order_by(Usuario.nome).all()

    return templates.TemplateResponse(
        request,
        "usuarios/index.html",
        {
            "request": request,
            "usuarios": usuarios,
            "admin": admin
        }
    )

# ... (mantenha os imports existentes)

# ROTA 1: Exibir o formulário de edição pré-preenchido
@router.get("/{usuario_id}/editar", response_class=HTMLResponse)
def exibir_formulario_editar(
    usuario_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin = Depends(get_admin)
):
    # Buscar o usuário que será editado
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        # Se não encontrar o usuário, pode redirecionar para a lista com um erro (opcional)
        return RedirectResponse(url="/usuarios", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        request,
        "usuarios/editar.html",  # Nome do novo arquivo HTML
        {
            "request": request,
            "usuario": usuario,
            "admin": admin
        }
    )


# ROTA 2: Processar a atualização dos dados do usuário
@router.post("/{usuario_id}/editar")
def processar_edicao_usuario(
    usuario_id: int,
    nome: str = Form(...),
    email: str = Form(...),
    role: str = Form(...),
    ativo: str = Form(None), # Checkbox envia valor se marcado, ou None se desmarcado
    senha: str = Form(None), # Senha opcional na edição
    db: Session = Depends(get_db),
    admin = Depends(get_admin)
):
    # Buscar o usuário no banco
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        return RedirectResponse(url="/usuarios", status_code=status.HTTP_303_SEE_OTHER)

    # Regra de segurança: Não permitir que o próprio admin logado se desative ou mude seu perfil
    is_auto_proprio = (usuario.id == admin.id)
    status_ativo = True if ativo == "on" else False

    if is_auto_proprio and (not status_ativo or role != admin.role):
        # Redireciona com erro se ele tentar se desativar ou mudar o próprio cargo nesta tela
        return RedirectResponse(url="/usuarios?erro=autoproprio", status_code=status.HTTP_303_SEE_OTHER)

    # Atualizar os campos comuns
    usuario.nome = nome
    usuario.email = email
    usuario.role = role
    usuario.ativo = status_ativo

    # Se uma nova senha foi digitada, faz o hash e atualiza
    if senha and senha.strip() != "":
        usuario.senha = hash_senha(senha) # Certifique-se que sua função hash_senha está importada corretamente

    # Salvar as alterações no banco de dados
    db.commit()

    # Redirecionar de volta para a lista com mensagem de sucesso
    return RedirectResponse(url="/usuarios?editado=ok", status_code=status.HTTP_303_SEE_OTHER)