"""
Router: Recomendaciones
Integra Prolog + IA Generativa para recomendaciones personalizadas
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.prolog_service import prolog_service
from app.services.ia_service import ia_service

router = APIRouter()

# Modelos
class CursosAprobadosRequest(BaseModel):
    cursosAprobados: List[str]

class RecomendacionCurso(BaseModel):
    codigo: str
    nombre: str
    creditos: int
    nivel: str
    area: str
    analisisProlog: List[str]
    explicacionIA: str

class Estadisticas(BaseModel):
    creditos: int
    cursosCompletados: int
    cursosDisponibles: int
    porcentajeProgreso: float

@router.post("/", response_model=List[RecomendacionCurso])
async def obtener_recomendaciones(request: CursosAprobadosRequest):
    """
    Obtener recomendaciones de cursos personalizadas
    Integra:
    1. Motor Prolog: Valida requisitos y obtiene cursos disponibles
    2. IA Generativa: Genera explicaciones en lenguaje natural
    """
    try:
        cursos_aprobados = request.cursosAprobados
        
        # 1. Consultar a Prolog los cursos disponibles
        codigos_disponibles = prolog_service.cursos_disponibles(cursos_aprobados)
        
        if not codigos_disponibles:
            return []
        
        # 2. Obtener información detallada y generar recomendaciones
        recomendaciones = []
        
        for codigo in codigos_disponibles:
            # Información del curso desde Prolog
            info = prolog_service.info_curso(codigo)
            
            if not info:
                continue
            
            # Obtener requisito
            requisito = prolog_service.requisito_de(codigo)
            
            # Análisis lógico de Prolog
            analisis_prolog = ia_service.generar_analisis_prolog(
                codigo=codigo,
                nombre=info['nombre'],
                requisito=requisito,
                cursos_aprobados=cursos_aprobados
            )
            
            # Explicación generada por IA
            explicacion_ia = ia_service.generar_explicacion_curso(
                codigo=codigo,
                nombre=info['nombre'],
                nivel=info['nivel'],
                area=info['area'],
                requisitos_cumplidos=True
            )
            
            # Crear recomendación completa
            recomendacion = RecomendacionCurso(
                codigo=codigo,
                nombre=info['nombre'],
                creditos=info['creditos'],
                nivel=info['nivel'],
                area=info['area'],
                analisisProlog=analisis_prolog,
                explicacionIA=explicacion_ia
            )
            
            recomendaciones.append(recomendacion)
        
        # Limitar a las primeras 10 recomendaciones para no saturar
        return recomendaciones[:10]
        
    except Exception as e:
        print(f"Error en recomendaciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/estadisticas", response_model=Estadisticas)
async def obtener_estadisticas(request: CursosAprobadosRequest):
    """
    Obtener estadísticas del progreso académico del estudiante
    """
    try:
        cursos_aprobados = request.cursosAprobados
        
        # Calcular créditos aprobados
        creditos_totales = 0
        for codigo in cursos_aprobados:
            info = prolog_service.info_curso(codigo)
            if info:
                creditos_totales += info['creditos']
        
        # Cursos disponibles
        cursos_disponibles = prolog_service.cursos_disponibles(cursos_aprobados)
        
        # Porcentaje de progreso
        porcentaje = prolog_service.porcentaje_progreso(cursos_aprobados)
        
        return Estadisticas(
            creditos=creditos_totales,
            cursosCompletados=len(cursos_aprobados),
            cursosDisponibles=len(cursos_disponibles),
            porcentajeProgreso=porcentaje
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/plan-academico")
async def generar_plan_academico(request: CursosAprobadosRequest):
    """
    Generar un plan académico personalizado usando IA
    """
    try:
        cursos_aprobados = request.cursosAprobados
        
        # Obtener cursos disponibles
        codigos_disponibles = prolog_service.cursos_disponibles(cursos_aprobados)
        
        # Obtener detalles de cursos disponibles
        cursos_detalle = []
        for codigo in codigos_disponibles:
            info = prolog_service.info_curso(codigo)
            if info:
                cursos_detalle.append(info)
        
        # Generar plan con IA
        plan = ia_service.generar_plan_academico(cursos_detalle, cursos_aprobados)
        
        return {
            "cursosAprobados": len(cursos_aprobados),
            "cursosDisponibles": len(cursos_detalle),
            "planSugerido": plan,
            "cursosRecomendados": cursos_detalle[:4]  # Top 4 recomendados
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/validar/{codigo}")
async def validar_curso_disponible(codigo: str, cursos_aprobados: List[str] = []):
    """
    Validar si un curso específico está disponible para el estudiante
    """
    try:
        puede_matricular = prolog_service.puede_matricular(codigo, cursos_aprobados)
        
        info = prolog_service.info_curso(codigo)
        requisito = prolog_service.requisito_de(codigo)
        
        return {
            "codigo": codigo,
            "puede_matricular": puede_matricular,
            "requisito": requisito,
            "info": info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))