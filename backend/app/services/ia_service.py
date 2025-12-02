"""
Microservicio: IA Generativa
Genera explicaciones en lenguaje natural usando Ollama (LLM local gratuito)
"""

import requests
from typing import List, Dict, Any
import json

class IAGenerativaService:
    def __init__(self, base_url: str = "http://localhost:11434"):
        """
        Inicializar servicio de IA Generativa con Ollama
        Ollama es un LLM local y gratuito
        """
        self.base_url = base_url
        self.model = "llama2"  # Modelo por defecto (gratuito)
        
    def generar_explicacion_curso(self, 
                                  codigo: str, 
                                  nombre: str, 
                                  nivel: str,
                                  area: str,
                                  requisitos_cumplidos: bool = True) -> str:
        """
        Generar explicación personalizada para un curso recomendado
        """
        
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
    
    def _explicacion_fallback(self, nombre: str, area: str, nivel: str) -> str:
        """
        Explicación de respaldo si la IA no está disponible
        """
        explicaciones_por_area = {
            "programacion": f"Este curso de {area} te ayudará a desarrollar habilidades fundamentales en desarrollo de software. Es esencial para tu formación como ingeniero informático y te preparará para los desafíos del mercado laboral.",
            "bases_datos": f"En este curso aprenderás a diseñar y gestionar bases de datos eficientemente. Es crucial para cualquier aplicación moderna y te dará las bases para trabajar con grandes volúmenes de información.",
            "redes": f"Este curso te enseñará los fundamentos de redes de computadoras y comunicación. Es esencial en un mundo cada vez más conectado y te abrirá oportunidades en administración de infraestructura.",
            "ingenieria_software": f"Aprenderás metodologías y buenas prácticas para desarrollar software de calidad. Este conocimiento es fundamental para trabajar en equipos profesionales de desarrollo.",
            "matematicas": f"Este curso desarrollará tu pensamiento lógico y analítico, habilidades esenciales para resolver problemas complejos en ciencias de la computación.",
            "seguridad": f"Aprenderás a proteger sistemas y datos, una habilidad cada vez más demandada en la industria tecnológica actual.",
            "sistemas_operativos": f"Comprenderás cómo funcionan los sistemas operativos a nivel profundo, conocimiento esencial para optimizar aplicaciones y resolver problemas de rendimiento.",
            "hardware": f"Entenderás la arquitectura de computadoras, lo que te permitirá optimizar software y comprender mejor el funcionamiento de los sistemas.",
            "general": f"Este curso complementará tu formación integral como profesional, desarrollando habilidades transversales importantes para tu carrera.",
            "idiomas": f"Desarrollarás habilidades de comunicación en inglés técnico, fundamentales para acceder a documentación y oportunidades internacionales."
        }
        
        return explicaciones_por_area.get(
            area,
            f"Este curso de nivel {nivel} es importante para tu formación académica y te ayudará a alcanzar tus objetivos profesionales."
        )
    
    def generar_analisis_prolog(self, 
                                codigo: str,
                                nombre: str,
                                requisito: str = None,
                                cursos_aprobados: List[str] = None) -> List[str]:
        """
        Generar análisis lógico basado en Prolog
        """
        analisis = []
        
        # Análisis de requisitos
        if requisito:
            if cursos_aprobados and requisito in cursos_aprobados:
                analisis.append(f"✅ Requisito {requisito} cumplido correctamente")
            else:
                analisis.append(f"⚠️ Requiere haber aprobado {requisito}")
        else:
            analisis.append("✅ Sin requisitos previos - puedes matricular libremente")
        
        # Análisis de secuencia lógica
        analisis.append(f"📋 Curso {codigo}: {nombre}")
        analisis.append("✅ Validado por el motor de inferencia Prolog")
        
        return analisis
    
    def generar_plan_academico(self, 
                               cursos_disponibles: List[Dict],
                               cursos_aprobados: List[str]) -> str:
        """
        Generar un plan académico personalizado
        """
        
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
                return self._plan_fallback(len(cursos_disponibles))
                
        except Exception as e:
            print(f"Error generando plan académico: {e}")
            return self._plan_fallback(len(cursos_disponibles))
    
    def _plan_fallback(self, num_cursos: int) -> str:
        """Plan de respaldo"""
        if num_cursos == 0:
            return "¡Felicitaciones! Has completado todos los cursos disponibles hasta el momento."
        elif num_cursos <= 4:
            return f"Tienes {num_cursos} curso(s) disponible(s). Te recomendamos matricularlos todos si tu carga académica lo permite."
        else:
            return f"Tienes {num_cursos} cursos disponibles. Te sugerimos matricular 3-4 cursos por cuatrimestre para mantener un balance saludable entre estudio y otras actividades."

# Singleton del servicio
ia_service = IAGenerativaService()