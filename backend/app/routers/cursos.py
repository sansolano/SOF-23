
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from app.services.prolog_service import prolog_service

router = APIRouter()

class CursoDetalle(BaseModel):
    codigo: str
    nombre: str
    creditos: int
    requisito: Optional[str]
    area: str
    nivel: str

class CursoPorArea(BaseModel):
    codigo: str
    nombre: str

@router.get("/", response_model=List[CursoDetalle])
async def obtener_todos_cursos():
    try:
        cursos = prolog_service.todos_los_cursos()
        return cursos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{codigo}", response_model=CursoDetalle)
async def obtener_curso(codigo: str):
    try:
        curso = prolog_service.info_curso(codigo)
        
        if not curso:
            raise HTTPException(
                status_code=404,
                detail=f"Curso {codigo} no encontrado"
            )
        
        # Obtener requisito
        requisito = prolog_service.requisito_de(codigo)
        curso["requisito"] = requisito
        
        return curso
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/area/{area}", response_model=List[CursoPorArea])
async def obtener_cursos_por_area(area: str):
  
    try:
        cursos = prolog_service.cursos_por_area(area)
        return cursos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/nivel/{nivel}", response_model=List[CursoPorArea])
async def obtener_cursos_por_nivel(nivel: str):
    
    try:
        cursos = prolog_service.cursos_por_nivel(nivel)
        return cursos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{codigo}/siguientes")
async def obtener_cursos_siguientes(codigo: str):
    
    try:
        siguientes = prolog_service.siguiente_curso(codigo)
        return {"codigo": codigo, "siguientes": siguientes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cuatrimestre/{numero}")
async def obtener_cursos_cuatrimestre(numero: int = Query(..., ge=1, le=12)):
    
    try:
        cursos = prolog_service.cursos_cuatrimestre(numero)
        
        # Obtener detalles de cada curso
        cursos_detalle = []
        for codigo in cursos:
            info = prolog_service.info_curso(codigo)
            if info:
                cursos_detalle.append(info)
        
        return {
            "cuatrimestre": numero,
            "cursos": cursos_detalle
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/totales")
async def obtener_estadisticas_carrera():
    try:
        total_creditos = prolog_service.total_creditos_carrera()
        total_cursos = prolog_service.total_cursos()
        
        return {
            "total_creditos": total_creditos,
            "total_cursos": total_cursos,
            "promedio_creditos_por_curso": round(total_creditos / total_cursos, 2) if total_cursos > 0 else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
