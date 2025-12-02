from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from app.models.curso import Recomendacion
from app.models.user import User
from app.routes.auth import get_current_user
from app.services.prolog_service import prolog_service
from app.services.ia_service import ia_service

router = APIRouter()

class RecomendacionRequest(BaseModel):
    cursosAprobados: List[str]

@router.post("/recomendaciones", response_model=List[Recomendacion])
async def generar_recomendaciones(
    request: RecomendacionRequest
):
    """
    Genera recomendaciones personalizadas usando Prolog + IA
    
    Este es el endpoint principal que:
    1. Consulta Prolog para obtener cursos disponibles
    2. Valida requisitos con lógica de Prolog
    3. Usa IA para generar explicaciones personalizadas
    """
    try:
        cursos_aprobados = request.cursosAprobados
        
        # PASO 1: Consultar Prolog para obtener cursos disponibles
        print(f"Consultando Prolog con cursos aprobados: {cursos_aprobados}")
        cursos_disponibles = prolog_service.get_cursos_disponibles(cursos_aprobados)
        
        print(f"Cursos disponibles desde Prolog: {cursos_disponibles}")
        
        if not cursos_disponibles:
            return []
        
        # PASO 2: Para cada curso disponible, obtener info y generar recomendación
        recomendaciones = []
        
        for codigo in cursos_disponibles[:10]:  # Limitar a 10 recomendaciones
            # Obtener información completa del curso
            curso_info = prolog_service.get_info_curso(codigo)
            
            if not curso_info:
                continue
            
            # PASO 3: Generar análisis lógico (Prolog)
            requisito = prolog_service.get_requisito(codigo)
            
            analisis_prolog = []
            
            # Análisis de requisitos
            if requisito == "ninguno":
                analisis_prolog.append("✓ No requiere cursos previos")
            else:
                analisis_prolog.append(f"✓ Requisito cumplido: {requisito}")
            
            # Análisis de nivel
            nivel = curso_info.get('nivel', '')
            if nivel == 'inicial':
                analisis_prolog.append("✓ Curso de nivel inicial, ideal para comenzar")
            elif nivel == 'intermedio':
                analisis_prolog.append("✓ Curso de nivel intermedio, construye sobre fundamentos")
            else:
                analisis_prolog.append("✓ Curso avanzado, profundiza conocimientos especializados")
            
            # Análisis de créditos
            creditos = curso_info.get('creditos', 0)
            analisis_prolog.append(f"✓ Aporta {creditos} créditos a tu carrera")
            
            # PASO 4: Generar explicación con IA
            print(f"Generando explicación IA para {codigo}...")
            explicacion_ia = ia_service.generar_explicacion(curso_info)
            
            # PASO 5: Crear objeto de recomendación
            recomendacion = Recomendacion(
                codigo=codigo,
                nombre=curso_info.get('nombre', ''),
                creditos=creditos,
                nivel=nivel,
                analisisProlog=analisis_prolog,
                explicacionIA=explicacion_ia
            )
            
            recomendaciones.append(recomendacion)
        
        print(f"Total de recomendaciones generadas: {len(recomendaciones)}")
        return recomendaciones
    
    except Exception as e:
        print(f"Error generando recomendaciones: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al generar recomendaciones: {str(e)}")

@router.get("/recomendaciones/optimizar-creditos")
async def optimizar_creditos(
    max_creditos: int = 12,
    current_user: User = Depends(get_current_user)
):
    """
    Sugiere una combinación de cursos que maximice créditos
    sin superar el límite especificado
    """
    try:
        cursos_aprobados = current_user.cursos_aprobados
        
        # Obtener cursos disponibles
        cursos_disponibles = prolog_service.get_cursos_disponibles(cursos_aprobados)
        
        # Obtener información de cada curso
        cursos_info = []
        for codigo in cursos_disponibles:
            info = prolog_service.get_info_curso(codigo)
            if info:
                cursos_info.append(info)
        
        # Algoritmo simple de optimización (greedy)
        # Ordenar por créditos descendente
        cursos_info.sort(key=lambda x: x.get('creditos', 0), reverse=True)
        
        seleccion = []
        creditos_totales = 0
        
        for curso in cursos_info:
            creditos_curso = curso.get('creditos', 0)
            if creditos_totales + creditos_curso <= max_creditos:
                seleccion.append(curso)
                creditos_totales += creditos_curso
        
        return {
            "cursos_recomendados": seleccion,
            "creditos_totales": creditos_totales,
            "max_creditos": max_creditos
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al optimizar créditos: {str(e)}")

@router.get("/recomendaciones/por-area/{area}")
async def recomendaciones_por_area(
    area: str,
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene recomendaciones filtradas por área temática
    """
    try:
        cursos_aprobados = current_user.cursos_aprobados
        
        # Obtener cursos disponibles
        cursos_disponibles = prolog_service.get_cursos_disponibles(cursos_aprobados)
        
        # Filtrar por área
        recomendaciones_area = []
        for codigo in cursos_disponibles:
            info = prolog_service.get_info_curso(codigo)
            if info and info.get('area', '') == area:
                recomendaciones_area.append(info)
        
        return recomendaciones_area
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener recomendaciones por área: {str(e)}")