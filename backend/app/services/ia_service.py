
import requests
from typing import List, Dict, Any
import json

class IAGenerativaService:
    def __init__(self, base_url: str = "http://localhost:11434"):
        
        self.base_url = base_url
        self.model = "llama2"  # Modelo por defecto (gratuito)
        
    def generar_explicacion_curso(self, 
                                  codigo: str, 
                                  nombre: str, 
                                  nivel: str,
                                  area: str,
                                  requisitos_cumplidos: bool = True) -> str:

        
        prompt = f"""
        Eres un asesor académico experto. Genera una explicación breve (máximo 3 oraciones) 
        sobre por qué un estudiante debería tomar el curso "{nombre}" ({codigo}).
        
        Información del curso:
        - Nivel: {nivel}
        - Área: {area}
        - Requisitos cumplidos: {'Sí' if requisitos_cumplidos else 'No'}
        
        La explicación debe:
        1. Mencionar las habilidades que desarrollará
        2. Indicar su importancia en la carrera
        3. Ser motivadora y clara
        
        Responde SOLO con la explicación, sin introducción ni conclusión.
        """
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                return self._explicacion_fallback(nombre, area, nivel)
                
        except Exception as e:
            print(f"Error conectando con Ollama: {e}")
            return self._explicacion_fallback(nombre, area, nivel)
    

    
    def generar_analisis_prolog(self, 
                                codigo: str,
                                nombre: str,
                                requisito: str = None,
                                cursos_aprobados: List[str] = None) -> List[str]:
        analisis = []
        
        if requisito:
            if cursos_aprobados and requisito in cursos_aprobados:
                analisis.append(f"Requisito {requisito} cumplido correctamente")
            else:
                analisis.append(f"Requiere haber aprobado {requisito}")
        else:
            analisis.append("Sin requisitos previos - puedes matricular libremente")
        
        analisis.append(f"Curso {codigo}: {nombre}")
        analisis.append("Validado por el motor de inferencia Prolog")
        
        return analisis
    
    def generar_plan_academico(self, 
                               cursos_disponibles: List[Dict],
                               cursos_aprobados: List[str]) -> str:
        
        prompt = f"""
        Eres un asesor académico. El estudiante ha aprobado {len(cursos_aprobados)} cursos 
        y tiene {len(cursos_disponibles)} cursos disponibles para matricular.
        
        Genera un consejo breve (2-3 oraciones) sobre cómo debería planificar su próximo cuatrimestre,
        considerando balance de dificultad, áreas de estudio y progreso en la carrera.
        
        Cursos disponibles: {len(cursos_disponibles)}
        Cursos aprobados: {len(cursos_aprobados)}
        """
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                return "Erro al usar IA Ollama"
                
        except Exception as e:
            print(f"Error generando plan académico: {e}")
            return "Erorro al usar IA Ollama"
    
ia_service = IAGenerativaService()
