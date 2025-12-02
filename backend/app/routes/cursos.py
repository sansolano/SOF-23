from fastapi import APIRouter, Depends, HTTPException
from typing import List
import json
from app.models.curso import Curso, CursoHistorial
from app.models.user import User
from app.routes.auth import get_current_user, load_users, save_users
from app.services.prolog_service import prolog_service

router = APIRouter()

@router.get("/cursos", response_model=List[Curso])
async def get_all_cursos():
    """
    Obtiene el catálogo completo de cursos
    """
    try:
        cursos = prolog_service.get_all_cursos()
        return cursos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener cursos: {str(e)}")

@router.get("/cursos/{codigo}")
async def get_curso(codigo: str):
    """
    Obtiene información de un curso específico
    """
    try:
        curso = prolog_service.get_info_curso(codigo)
        
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        
        return curso
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener curso: {str(e)}")

@router.get("/estadisticas")
async def get_estadisticas(current_user: User = Depends(get_current_user)):
    """
    Obtiene estadísticas del estudiante
    """
    try:
        cursos_aprobados = current_user.cursos_aprobados
        cursos_en_curso = current_user.cursos_en_curso
        
        # Calcular créditos
        creditos_totales = 0
        for codigo in cursos_aprobados:
            curso = prolog_service.get_info_curso(codigo)
            if curso:
                creditos_totales += curso.get('creditos', 0)
        
        # Obtener cursos disponibles
        cursos_disponibles = prolog_service.get_cursos_disponibles(cursos_aprobados)
        
        return {
            "creditos": creditos_totales,
            "cursosCompletados": len(cursos_aprobados),
            "cursosEnCurso": len(cursos_en_curso),
            "cursosDisponibles": len(cursos_disponibles)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

@router.get("/historial")
async def get_historial(current_user: User = Depends(get_current_user)):
    """
    Obtiene el historial académico completo del estudiante
    """
    try:
        cursos_aprobados = current_user.cursos_aprobados
        cursos_en_curso = current_user.cursos_en_curso
        
        # Obtener información completa de cursos aprobados
        historial_aprobados = []
        for codigo in cursos_aprobados:
            curso = prolog_service.get_info_curso(codigo)
            if curso:
                historial_aprobados.append({
                    **curso,
                    "estado": "aprobado"
                })
        
        # Obtener información completa de cursos en curso
        historial_en_curso = []
        for codigo in cursos_en_curso:
            curso = prolog_service.get_info_curso(codigo)
            if curso:
                historial_en_curso.append({
                    **curso,
                    "estado": "en-curso"
                })
        
        # Obtener cursos pendientes (disponibles)
        disponibles = prolog_service.get_cursos_disponibles(cursos_aprobados)
        historial_pendientes = []
        for codigo in disponibles:
            if codigo not in cursos_en_curso:  # No incluir cursos en curso
                curso = prolog_service.get_info_curso(codigo)
                if curso:
                    requisito = prolog_service.get_requisito(codigo)
                    historial_pendientes.append({
                        **curso,
                        "estado": "pendiente",
                        "requisito": requisito
                    })
        
        return {
            "aprobados": historial_aprobados,
            "en_curso": historial_en_curso,
            "pendientes": historial_pendientes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener historial: {str(e)}")

@router.post("/historial")
async def agregar_curso_historial(
    curso_data: CursoHistorial,
    current_user: User = Depends(get_current_user)
):
    """
    Agrega un curso al historial del estudiante
    """
    try:
        # Cargar usuarios
        data = load_users()
        
        # Buscar usuario
        user_index = next((i for i, u in enumerate(data["users"]) if u["email"] == current_user.email), None)
        
        if user_index is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Actualizar historial según el estado
        if curso_data.estado == "aprobado":
            if curso_data.curso not in data["users"][user_index]["cursos_aprobados"]:
                data["users"][user_index]["cursos_aprobados"].append(curso_data.curso)
            # Remover de en_curso si estaba
            if curso_data.curso in data["users"][user_index]["cursos_en_curso"]:
                data["users"][user_index]["cursos_en_curso"].remove(curso_data.curso)
        
        elif curso_data.estado == "en-curso":
            if curso_data.curso not in data["users"][user_index]["cursos_en_curso"]:
                data["users"][user_index]["cursos_en_curso"].append(curso_data.curso)
        
        # Guardar cambios
        save_users(data)
        
        return {"message": "Curso agregado exitosamente", "curso": curso_data.curso}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar curso: {str(e)}")

@router.delete("/historial/{codigo}")
async def eliminar_curso_historial(
    codigo: str,
    current_user: User = Depends(get_current_user)
):
    """
    Elimina un curso del historial del estudiante
    """
    try:
        # Cargar usuarios
        data = load_users()
        
        # Buscar usuario
        user_index = next((i for i, u in enumerate(data["users"]) if u["email"] == current_user.email), None)
        
        if user_index is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Remover de ambas listas
        if codigo in data["users"][user_index]["cursos_aprobados"]:
            data["users"][user_index]["cursos_aprobados"].remove(codigo)
        
        if codigo in data["users"][user_index]["cursos_en_curso"]:
            data["users"][user_index]["cursos_en_curso"].remove(codigo)
        
        # Guardar cambios
        save_users(data)
        
        return {"message": "Curso eliminado exitosamente", "curso": codigo}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar curso: {str(e)}")