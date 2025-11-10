from fastapi import Depends, HTTPException, Request
from sqlmodel import Session
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from db.database import get_session
from db.models import User, UserRole
from passlib.context import CryptContext

# Configuration du contexte bcrypt pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "ceci est une phrase tres secrete"
ALGORITHM = "HS256"
COOKIE_NAME = "access_token"

def hash_password(password: str) -> str:
    """Hache un mot de passe avec bcrypt."""
    # Limiter le mot de passe à 72 bytes (limite de bcrypt)
    password_truncated = password[:72]
    return pwd_context.hash(password_truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe en le comparant avec son hash."""
    # Limiter le mot de passe à 72 bytes (limite de bcrypt)
    password_truncated = plain_password[:72]
    return pwd_context.verify(password_truncated, hashed_password)

def create_access_token(data: dict):
    """Crée un token JWT sécurisé (badge)"""
    to_encode = data.copy()
    # Le badge expire après 1 jour
    expire = datetime.now(timezone.utc) + timedelta(days=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_from_cookie(
    request: Request, 
    session: Session = Depends(get_session)
) -> User:
    """
    Dépendance FastAPI : lit le cookie, décode le token, 
    et retourne l'utilisateur.
    Sinon, redirige vers /login.
    """
    token = request.cookies.get(COOKIE_NAME)
    
    if not token:
        # Si pas de badge, redirection vers login
        raise HTTPException(status_code=303, detail="Not authenticated", headers={"Location": "/login"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub") # "sub" est le nom standard pour l'ID utilisateur
        if user_id is None:
            raise HTTPException(status_code=303, detail="Invalid token", headers={"Location": "/login"})
            
    except JWTError:
        # Si le badge est invalide ou expiré, on redirige vers login
        raise HTTPException(status_code=303, detail="Invalid token", headers={"Location": "/login"})

    user = session.get(User, int(user_id))
    if user is None:
        raise HTTPException(status_code=303, detail="User not found", headers={"Location": "/login"})
        
    # Si tout va bien, on retourne l'objet User
    return user

# --- Dépendance pour les Admins  ---
def is_admin(user: User = Depends(get_current_user_from_cookie)):
    """
    Dépendance qui vérifie si l'utilisateur actuel est un Admin.
    """
    if user.user_role != UserRole.ADMIN:
        # Si ce n'est pas un admin, on lève une erreur 403 (Accès Interdit)
        raise HTTPException(status_code=403, detail="Accès non autorisé : réservé aux admins.")
    return user