from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
import json
import os
from app.models.user import User, UserLogin, UserRegister, Token
from app.utils.auth_utils import verify_password, create_access_token, decode_access_token, hash_password

router = APIRouter()

# Ruta del archivo de usuarios
USERS_FILE = "data/users.json"

def load_users():
    """Carga los usuarios del archivo JSON"""
    if not os.path.exists(USERS_FILE):
        return {"users": []}
    
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(data):
    """Guarda los usuarios en el archivo JSON"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_current_user(authorization: Optional[str] = Header(None)) -> User:
    """Obtiene el usuario actual desde el token JWT"""
    if not authorization:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    try:
        # El token viene como "Bearer <token>"
        token = authorization.replace("Bearer ", "")
        payload = decode_access_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        
        # Cargar datos del usuario
        data = load_users()
        user_email = payload.get("sub")
        
        user_data = next((u for u in data["users"] if u["email"] == user_email), None)
        
        if not user_data:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return User(**{k: v for k, v in user_data.items() if k != 'password'})
    
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Endpoint de login
    - Verifica email y contraseña
    - Retorna token JWT y datos del usuario
    """
    data = load_users()
    
    # Buscar usuario por email
    user = next((u for u in data["users"] if u["email"] == credentials.email), None)
    
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Verificar contraseña
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Crear token
    token = create_access_token(data={"sub": user["email"]})
    
    # Preparar datos del usuario (sin password)
    user_data = {k: v for k, v in user.items() if k != 'password'}
    
    return {
        "token": token,
        "user": user_data
    }

@router.post("/register", response_model=Token)
async def register(user_data: UserRegister):
    """
    Endpoint de registro
    - Crea un nuevo usuario
    - Retorna token JWT
    """
    data = load_users()
    
    # Verificar si el email ya existe
    if any(u["email"] == user_data.email for u in data["users"]):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Crear nuevo usuario
    new_user = {
        "id": f"EST{str(len(data['users']) + 1).zfill(3)}",
        "nombre": user_data.nombre,
        "email": user_data.email,
        "password": hash_password(user_data.password),
        "carrera": user_data.carrera,
        "cursos_aprobados": [],
        "cursos_en_curso": []
    }
    
    data["users"].append(new_user)
    save_users(data)
    
    # Crear token
    token = create_access_token(data={"sub": new_user["email"]})
    
    # Preparar datos del usuario (sin password)
    user_response = {k: v for k, v in new_user.items() if k != 'password'}
    
    return {
        "token": token,
        "user": user_response
    }

@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Obtiene los datos del usuario actual
    """
    return current_user