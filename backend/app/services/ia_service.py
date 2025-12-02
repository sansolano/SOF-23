import ollama
from typing import Dict

class IAService:
    """
    Servicio para generar explicaciones usando IA generativa (Ollama)
    """
    
    def __init__(self, model: str = "llama3.2:1b"):
        self.model = model
    
    def generar_explicacion(self, curso_info: Dict[str, any]) -> str:
        """
        Genera una explicación personalizada para un curso recomendado
        """
        codigo = curso_info.get('codigo', '')
        nombre = curso_info.get('nombre', '')
        area = curso_info.get('area', '')
        nivel = curso_info.get('nivel', '')
        creditos = curso_info.get('creditos', 0)
        
        # Crear prompt para la IA
        prompt = f"""Eres un asesor académico universitario experto. Genera una explicación breve y motivadora (máximo 3 oraciones) sobre el siguiente curso recomendado:

Curso: {codigo} - {nombre}
Área: {area}
Nivel: {nivel}
Créditos: {creditos}

La explicación debe:
1. Explicar por qué este curso es importante para la carrera
2. Mencionar habilidades o conocimientos que desarrollará
3. Ser clara, concisa y motivadora

Responde SOLO con la explicación, sin saludos ni introducciones."""

        try:
            # Llamar a Ollama
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            explicacion = response['message']['content'].strip()
            return explicacion
        
        except Exception as e:
            print(f"Error llamando a Ollama: {e}")
            # Fallback: explicación genérica
            return self._generar_explicacion_fallback(curso_info)
    
    def _generar_explicacion_fallback(self, curso_info: Dict[str, any]) -> str:
        """
        Genera una explicación básica sin IA
        """
        nombre = curso_info.get('nombre', '')
        area = curso_info.get('area', '')
        nivel = curso_info.get('nivel', '')
        
        explicaciones_area = {
            'programacion': f"Este curso de {nivel} te permitirá dominar técnicas avanzadas de programación esenciales para tu desarrollo como ingeniero. Aprenderás conceptos y prácticas que utilizarás durante toda tu carrera profesional.",
            'bases_datos': f"Este curso de {nivel} te enseñará a diseñar y gestionar bases de datos eficientes, una habilidad fundamental en el desarrollo de aplicaciones modernas. Dominar estos conceptos te abrirá puertas en múltiples áreas de la informática.",
            'ingenieria_software': f"Este curso de {nivel} te preparará para trabajar en proyectos de software reales, aplicando metodologías y mejores prácticas de la industria. Es fundamental para tu formación como ingeniero de software profesional.",
            'redes': f"Este curso de {nivel} te dará las bases para entender cómo funcionan las comunicaciones en Internet y las redes modernas. Conocimientos esenciales en la era digital actual.",
            'matematicas': f"Este curso de {nivel} te proporcionará las herramientas matemáticas necesarias para resolver problemas complejos en computación. Es fundamental para cursos más avanzados.",
            'general': f"Este curso de {nivel} complementará tu formación integral como profesional, desarrollando habilidades importantes más allá de lo técnico."
        }
        
        return explicaciones_area.get(area, f"Este curso de {nombre} es importante para tu desarrollo profesional y te permitirá adquirir competencias valiosas en {area}.")

# Instancia global del servicio
ia_service = IAService()