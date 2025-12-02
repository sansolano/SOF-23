from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, cursos, recomendaciones

# Crear la aplicación FastAPI
app = FastAPI(
    title="Asistente Académico API",
    description="API para el sistema de recomendaciones académicas con Prolog e IA",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(cursos.router, prefix="/api", tags=["Cursos"])
app.include_router(recomendaciones.router, prefix="/api", tags=["Recomendaciones"])

# Ruta raíz
@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API del Asistente Académico",
        "version": "1.0.0",
        "status": "online"
    }

# Ruta de salud
@app.get("/health")
def health_check():
    return {"status": "healthy"}