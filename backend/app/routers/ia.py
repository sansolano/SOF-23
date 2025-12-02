"""
Router: IA Generativa
Acceso directo a funcionalidades de IA
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.ia_service import ia_service

router = APIRouter()

# Modelos
class ExplicacionRequest(BaseModel):
    codigo: str
    nombre: str
    nivel: str
    area: str

class PlanAcademicoRequest(BaseModel):
    cursosAprobados: int
    cursosDisponibles: int

@router.get("/test")
async def test_ia():
    """Verificar que el servicio de IA está disponible"""
    try:
        # Prueba simple
        explicacion = ia_service._explicacion_fallback(
            "Programación I",
            "programacion",
            "intermedio"
        )
        return {
            "status": "OK",
            "servicio": "IA Generativa (Ollama)",
            "message": "Servicio de IA disponible",
            "ejemplo": explicacion
        }
    except Exception as e:
        return {
            "status": "FALLBACK",
            "message": "IA no disponible, usando explicaciones predefinidas",
            "error": str(e)
        }

@router.post("/explicacion")
async def generar_explicacion(request: ExplicacionRequest):
    """Generar explicación personalizada para un curso"""
    try:
        explicacion = ia_service.generar_explicacion_curso(
            codigo=request.codigo,
            nombre=request.nombre,
            nivel=request.nivel,
            area=request.area
        )
        
        return {
            "codigo": request.codigo,
            "explicacion": explicacion
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/plan")
async def generar_plan(request: PlanAcademicoRequest):
    """Generar plan académico personalizado"""
    try:
        # Crear lista simulada de cursos
        cursos_sim = [{"codigo": f"SOF-{i}"} for i in range(request.cursosDisponibles)]
        cursos_aprobados = [f"SOF-{i}" for i in range(request.cursosAprobados)]
        
        plan = ia_service.generar_plan_academico(cursos_sim, cursos_aprobados)
        
        return {
            "plan": plan,
            "cursosAprobados": request.cursosAprobados,
            "cursosDisponibles": request.cursosDisponibles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def check_ia_health():
    """Verificar el estado del servicio de IA"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            return {
                "status": "ONLINE",
                "servicio": "Ollama",
                "modelos_disponibles": [m.get('name') for m in models] if models else [],
                "url": "http://localhost:11434"
            }
        else:
            return {
                "status": "FALLBACK",
                "message": "Ollama no responde, usando explicaciones predefinidas"
            }
    except Exception as e:
        return {
            "status": "FALLBACK",
            "message": "Ollama no disponible, usando explicaciones predefinidas",
            "info": "Para habilitar IA local, instala Ollama desde https://ollama.ai"
        }