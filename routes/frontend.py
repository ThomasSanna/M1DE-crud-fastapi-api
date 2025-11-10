from fastapi import APIRouter, Form, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select, func
from datetime import datetime
from db.database import get_session
from models import User, Produit, UserRole
from fastapi.templating import Jinja2Templates
from security import create_access_token, get_current_user_from_cookie

templates = Jinja2Templates(directory="templates")
router = APIRouter()

# Endpoints API Frontend

@router.get("/", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
def login_user(request: Request, email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.user_mail==email, User.user_password==password)).first()
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Email ou mot de passe invalide"})
    user.user_date_login = datetime.now()
    session.add(user)
    session.commit()

    token_data = {"sub": str(user.user_id), "role": user.user_role}
    access_token = create_access_token(data=token_data)

    if user.user_role == UserRole.ADMIN:
        redirect_url = "/admin/"  # Le hub du backoffice
    else:
        redirect_url = "/produits"

    response = RedirectResponse(url=redirect_url, status_code=303)
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True # Important pour la sécurité
    )
    return response

@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
def register_user(request: Request, email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.user_mail==email)).first()
    if existing:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email déjà utilisée"})
    #ajout user_compte_id
    max_id = session.scalar(select(func.max(User.user_compte_id)))
    new_compte_id = (max_id or 0) + 1

    user = User(user_login=email, 
                user_mail=email, 
                user_password=password, 
                user_compte_id=new_compte_id, 
                user_date_new=datetime.now(), 
                user_date_login=datetime.now()
                )
    session.add(user)
    session.commit()
    return RedirectResponse("/login", status_code=303)


@router.get("/produits", response_class=HTMLResponse)
def produits_list(request: Request, session: Session = Depends(get_session)):
    produits = session.exec(select(Produit)).all()
    # produits is a list of Produit objects; pass to template
    return templates.TemplateResponse("produits.html", {"request": request, "produits": produits})

@router.get("/profil", response_class=HTMLResponse)
def get_profil(
    request: Request, 
    user: User = Depends(get_current_user_from_cookie), 
    message: str | None = None, 
    error: bool = False
):
    """Affiche la page de profil."""
    return templates.TemplateResponse("profil.html", {
        "request": request, 
        "user": user,
        "message": message,
        "error": error
    })


@router.post("/profil", response_class=RedirectResponse)
def update_profil(
    request: Request,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user_from_cookie), 
    user_login: str = Form(...),
    user_mail: str = Form(...),
    user_password: str | None = Form(None) 
):
    
    # Vérifie si le nouvel email est déjà pris par quelqu'un d'autre
    existing_user = session.exec(select(User).where(User.user_mail == user_mail, User.user_id != user.user_id)).first()
    if existing_user:
        return RedirectResponse(url="/profil?error=true&message=Cet email est déjà utilisé.", status_code=303)

    user.user_login = user_login
    user.user_mail = user_mail
    if user_password: 
        user.user_password = user_password
        
    session.add(user)
    session.commit()

    return RedirectResponse(url="/profil?message=Profil mis à jour avec succès !", status_code=303)

@router.get("/logout")
def logout():
    """
    Déconnecte l'utilisateur en supprimant le badge (cookie).
    """
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    return response



