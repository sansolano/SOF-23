
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


@router.post("/explicacion")
async def generar_explicacion(request: ExplicacionRequest):
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
