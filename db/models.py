from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(SQLModel, table=True):
    __tablename__ = "user"
    user_id: int | None = Field(default=None, primary_key=True)
    user_login: str
    user_password: str
    user_mail: str
    user_compte_id : int 
    user_date_new: datetime
    user_date_login: datetime | None = None
    user_role: str = Field(default=UserRole.USER)


class Produit(SQLModel, table=True):
    __tablename__ = "produit"
    id_p: int   | None = Field(default=None, primary_key=True)
    type_p: str
    designation_p: str
    #description_p: str | None = None
    prix_ht: float
    date_in: datetime
    timeS_in: datetime
    stock_p: int
    image_p: str = Field(default="default.png")
    ppromo: float | None = Field(default=None)

class ProduitForm(BaseModel):
    """Modèle Pydantic pour le formulaire Produit"""
    type_p: str
    designation_p: str
    #description_p : str
    prix_ht: float
    stock_p: int
    ppromo: float | None  = None

class UserForm(BaseModel):
    """Modèle Pydantic pour le formulaire User"""
    user_login: str
    user_mail: str
    user_password: str
    user_role: UserRole

class UserUpdateForm(BaseModel):
    """Modèle Pydantic pour la mise à jour d'un User"""
    user_login: str
    user_mail: str
    user_role: UserRole