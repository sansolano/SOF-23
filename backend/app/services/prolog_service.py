from pyswip import Prolog
from typing import List, Dict, Any, Optional
import os

class PrologService:
    def __init__(self, prolog_file_path: str = "cursos.pl"):
        """Inicializar el motor Prolog"""
        self.prolog = Prolog()
        
        if os.path.exists(prolog_file_path):
            self.prolog.consult(prolog_file_path)
            print(f"Archivo cargado: {prolog_file_path}")
        else:
            raise FileNotFoundError(f"No se encontró el archivo: {prolog_file_path}")
    
    def puede_matricular(self, codigo_curso: str, cursos_aprobados: List[str]) -> bool:

        try:
            # Convertir lista a formato Prolog
            cursos_str = str(cursos_aprobados).replace("'", "'")
            
            query = f"puede_matricular(_, '{codigo_curso}', {cursos_str})"
            result = list(self.prolog.query(query))
            
            return len(result) > 0
        except Exception as e:
            print(f"Error en puede_matricular: {e}")
            return False
    
    def cursos_disponibles(self, cursos_aprobados: List[str]) -> List[str]:

        try:
            cursos_str = str(cursos_aprobados).replace("'", "'")
            
            query = f"cursos_disponibles(_, {cursos_str}, ListaCursos)"
            results = list(self.prolog.query(query))
            
            if results:
                return results[0]['ListaCursos']
            return []
        except Exception as e:
            print(f"Error en cursos_disponibles: {e}")
            return []
    
    def info_curso(self, codigo_curso: str) -> Optional[Dict[str, Any]]:

        try:
            query = f"info_curso('{codigo_curso}', Nombre, Creditos, Area, Nivel)"
            results = list(self.prolog.query(query))
            
            if results:
                result = results[0]
                return {
                    "codigo": codigo_curso,
                    "nombre": result['Nombre'],
                    "creditos": result['Creditos'],
                    "area": str(result['Area']),
                    "nivel": str(result['Nivel'])
                }
            return None
        except Exception as e:
            print(f"Error en info_curso: {e}")
            return None
    
    def requisito_de(self, codigo_curso: str) -> Optional[str]:

        try:
            query = f"requisito_de('{codigo_curso}', Requisito)"
            results = list(self.prolog.query(query))
            
            if results:
                req = results[0]['Requisito']
                return None if str(req) == 'ninguno' else str(req)
            return None
        except Exception as e:
            print(f"Error en requisito_de: {e}")
            return None
    
    def cursos_por_area(self, area: str) -> List[Dict[str, str]]:

        try:
            query = f"cursos_por_area({area}, ListaCursos)"
            results = list(self.prolog.query(query))
            
            if results:
                cursos = results[0]['ListaCursos']
                return [
                    {"codigo": c[0], "nombre": c[1]} 
                    for c in cursos
                ]
            return []
        except Exception as e:
            print(f"Error en cursos_por_area: {e}")
            return []
    
    def cursos_por_nivel(self, nivel: str) -> List[Dict[str, str]]:

        try:
            query = f"cursos_por_nivel({nivel}, ListaCursos)"
            results = list(self.prolog.query(query))
            
            if results:
                cursos = results[0]['ListaCursos']
                return [
                    {"codigo": c[0], "nombre": c[1]} 
                    for c in cursos
                ]
            return []
        except Exception as e:
            print(f"Error en cursos_por_nivel: {e}")
            return []
    
    def siguiente_curso(self, codigo_curso_actual: str) -> List[Dict[str, str]]:

        try:
            query = f"siguiente_curso('{codigo_curso_actual}', Codigo, Nombre)"
            results = list(self.prolog.query(query))
            
            return [
                {"codigo": r['Codigo'], "nombre": r['Nombre']} 
                for r in results
            ]
        except Exception as e:
            print(f"Error en siguiente_curso: {e}")
            return []
    
    def total_creditos_carrera(self) -> int:

        try:
            query = "total_creditos_carrera(Total)"
            results = list(self.prolog.query(query))
            
            if results:
                return results[0]['Total']
            return 0
        except Exception as e:
            print(f"Error en total_creditos_carrera: {e}")
            return 0
    
    def total_cursos(self) -> int:
  
        try:
            query = "total_cursos(Total)"
            results = list(self.prolog.query(query))
            
            if results:
                return results[0]['Total']
            return 0
        except Exception as e:
            print(f"Error en total_cursos: {e}")
            return 0
    
    def porcentaje_progreso(self, cursos_aprobados: List[str]) -> float:

        try:
            cursos_str = str(cursos_aprobados).replace("'", "'")
            
            query = f"porcentaje_progreso({cursos_str}, Porcentaje)"
            results = list(self.prolog.query(query))
            
            if results:
                return round(results[0]['Porcentaje'], 2)
            return 0.0
        except Exception as e:
            print(f"Error en porcentaje_progreso: {e}")
            return 0.0
    
    def cursos_cuatrimestre(self, num_cuatrimestre: int) -> List[str]:

        try:
            query = f"cursos_cuatrimestre({num_cuatrimestre}, ListaCursos)"
            results = list(self.prolog.query(query))
            
            if results:
                return results[0]['ListaCursos']
            return []
        except Exception as e:
            print(f"Error en cursos_cuatrimestre: {e}")
            return []
    
    def todos_los_cursos(self) -> List[Dict[str, Any]]:
    
        try:
            query = "curso(Codigo, Nombre, Creditos, Requisito, Area, Nivel)"
            results = list(self.prolog.query(query))
            
            cursos = []
            for r in results:
                cursos.append({
                    "codigo": r['Codigo'],
                    "nombre": r['Nombre'],
                    "creditos": r['Creditos'],
                    "requisito": None if str(r['Requisito']) == 'ninguno' else str(r['Requisito']),
                    "area": str(r['Area']),
                    "nivel": str(r['Nivel'])
                })
            
            return cursos
        except Exception as e:
            print(f"Error en todos_los_cursos: {e}")
            return []

# Singleton del servicio
prolog_service = PrologService()
