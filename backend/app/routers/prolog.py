
from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.prolog_service import prolog_service

router = APIRouter()


@router.get("/puede-matricular/{codigo}")
async def verificar_puede_matricular(
    codigo: str,
    cursos_aprobados: List[str] = Query(default=[])
):
    """Verificar si puede matricular un curso específico"""
    try:
        puede = prolog_service.puede_matricular(codigo, cursos_aprobados)
        requisito = prolog_service.requisito_de(codigo)
        
        return {
            "codigo": codigo,
            "puede_matricular": puede,
            "requisito_previo": requisito,
            "cursos_aprobados": cursos_aprobados
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cursos-disponibles")
async def obtener_cursos_disponibles(
    cursos_aprobados: List[str] = Query(default=[])
):
    try:
        disponibles = prolog_service.cursos_disponibles(cursos_aprobados)
        
        # Obtener detalles de cada curso
        cursos_detalle = []
        for codigo in disponibles:
            info = prolog_service.info_curso(codigo)
            if info:
                cursos_detalle.append(info)
        
        return {
            "cursos_aprobados": len(cursos_aprobados),
            "cursos_disponibles": len(disponibles),
            "cursos": cursos_detalle
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/progreso")
async def calcular_progreso(
    cursos_aprobados: List[str] = Query(default=[])
):
    try:
        porcentaje = prolog_service.porcentaje_progreso(cursos_aprobados)
        total_cursos = prolog_service.total_cursos()
        total_creditos = prolog_service.total_creditos_carrera()
        
        # Calcular créditos aprobados
        creditos_aprobados = 0
        for codigo in cursos_aprobados:
            info = prolog_service.info_curso(codigo)
            if info:
                creditos_aprobados += info['creditos']
        
        return {
            "cursos_aprobados": len(cursos_aprobados),
            "total_cursos": total_cursos,
            "porcentaje_cursos": porcentaje,
            "creditos_aprobados": creditos_aprobados,
            "total_creditos": total_creditos,
            "porcentaje_creditos": round((creditos_aprobados / total_creditos) * 100, 2) if total_creditos > 0 else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
