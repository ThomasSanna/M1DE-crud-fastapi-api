from datetime import datetime
from fastapi import APIRouter, Form, Depends, HTTPException
from sqlmodel import Session, select
from db.models import User
from db.database import get_session
from security import hash_password

router = APIRouter(prefix="/api")

# Endpoints API Backend

@router.get("/users")
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@router.get("/users/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users")
def create_user(email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.user_mail==email)).first():
        raise HTTPException(status_code=400, detail="Email already in use")
    user = User(user_login=email, user_mail=email, user_password=hash_password(password), user_date_new=datetime.now())
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User created", "user_id": user.user_id}

@router.put("/users/{user_id}")
def update_user(user_id: int, email: str | None = Form(None), password: str | None = Form(None), session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if email:
        user.user_login = email
        user.user_mail = email
    if password:
        user.user_password = hash_password(password)
    session.add(user)
    session.commit()
    return {"message": "User updated", "user_id": user.user_id}

@router.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": f"User {user_id} deleted"}


# Produit endpoints
from db.models import Produit


@router.get("/produits")
def get_produits(type_p: str | None = None, session: Session = Depends(get_session)):
    """Récupère tous les produits, avec possibilité de filtrer par type"""
    query = select(Produit)
    if type_p:
        query = query.where(Produit.type_p == type_p)
    return session.exec(query).all()


@router.get("/produits/types")
def get_product_types(session: Session = Depends(get_session)):
    """Récupère la liste des types de produits disponibles"""
    from sqlmodel import col
    types = session.exec(select(Produit.type_p).distinct()).all()
    return {"types": sorted(list(set(types)))}


@router.get("/produits/{id_p}")
def get_produit(id_p: int, session: Session = Depends(get_session)):
    prod = session.get(Produit, id_p)
    if not prod:
        raise HTTPException(status_code=404, detail="Produit not found")
    return prod


@router.post("/produits")
def create_produit(type_p: str = Form(...), designation_p: str = Form(...), description_p: str | None = Form(None), prix_ht: float = Form(...), stock_p: int = Form(...), session: Session = Depends(get_session)):
    # naive creation
    prod = Produit(type_p=type_p, designation_p=designation_p, description_p=description_p, prix_ht=prix_ht, date_in=datetime.now(), timeS_in=datetime.now(), stock_p=stock_p)
    session.add(prod)
    session.commit()
    session.refresh(prod)
    return {"message": "Produit created", "id_p": prod.id_p}


@router.put("/produits/{id_p}")
def update_produit(id_p: int, type_p: str | None = Form(None), designation_p: str | None = Form(None), description_p: str | None = Form(None), prix_ht: float | None = Form(None), stock_p: int | None = Form(None), session: Session = Depends(get_session)):
    prod = session.get(Produit, id_p)
    if not prod:
        raise HTTPException(status_code=404, detail="Produit not found")
    if type_p is not None:
        prod.type_p = type_p
    if designation_p is not None:
        prod.designation_p = designation_p
    if description_p is not None:
        prod.description_p = description_p
    if prix_ht is not None:
        prod.prix_ht = prix_ht
    if stock_p is not None:
        prod.stock_p = stock_p
    session.add(prod)
    session.commit()
    return {"message": "Produit updated", "id_p": prod.id_p}


@router.delete("/produits/{id_p}")
def delete_produit(id_p: int, session: Session = Depends(get_session)):
    prod = session.get(Produit, id_p)
    if not prod:
        raise HTTPException(status_code=404, detail="Produit not found")
    session.delete(prod)
    session.commit()
    return {"message": f"Produit {id_p} deleted"}
