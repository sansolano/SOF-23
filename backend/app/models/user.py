from pydantic import BaseModel, EmailStr
from typing import List, Optional

class User(BaseModel):
    id: str
    nombre: str
    email: EmailStr
    carrera: str
    cursos_aprobados: List[str] = []
    cursos_en_curso: List[str] = []

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    carrera: str = "Ingeniería Informática"

class Token(BaseModel):
    token: str
    user: User