import subprocess
import re
from typing import List, Dict, Any

class PrologService:
    """
    Servicio para comunicarse con Prolog
    Usa subprocess para ejecutar SWI-Prolog directamente
    """
    
    def __init__(self, prolog_file: str = "cursos.pl"):
        self.prolog_file = prolog_file
        self.swipl_path = "swipl"  # Asume que swipl está en PATH
    
    def _execute_query(self, query: str) -> str:
        """
        Ejecuta una consulta Prolog y retorna el resultado
        """
        try:
            # Crear script temporal con la consulta
            prolog_script = f"""
            :- initialization(main).
            :- consult('{self.prolog_file}').
            
            main :-
                {query},
                halt.
            main :-
                write('false'),
                halt(1).
            """
            
            # Ejecutar con SWI-Prolog
            result = subprocess.run(
                [self.swipl_path, "-g", f"{query}, halt", "-t", "halt(1)", self.prolog_file],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            return result.stdout.strip()
        
        except subprocess.TimeoutExpired:
            return "timeout"
        except FileNotFoundError:
            # Si SWI-Prolog no está instalado, usar implementación Python
            return self._fallback_query(query)
        except Exception as e:
            print(f"Error ejecutando Prolog: {e}")
            return ""
    
    def _fallback_query(self, query: str) -> str:
        """
        Implementación alternativa en Python puro (sin Prolog real)
        Para desarrollo cuando Prolog no está disponible
        """
        # Base de datos simplificada en Python
        cursos_db = self._load_cursos_from_pl()
        
        # Detectar tipo de consulta
        if "cursos_disponibles" in query:
            return self._get_cursos_disponibles_fallback(query, cursos_db)
        elif "info_curso" in query:
            return self._get_info_curso_fallback(query, cursos_db)
        
        return ""
    
    def _load_cursos_from_pl(self) -> List[Dict]:
        """
        Parsea el archivo .pl y extrae los cursos
        """
        cursos = []
        try:
            with open(self.prolog_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extraer cursos con regex
            pattern = r"curso\('([^']+)',\s*'([^']+)',\s*(\d+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)"
            matches = re.findall(pattern, content)
            
            for match in matches:
                cursos.append({
                    'codigo': match[0],
                    'nombre': match[1],
                    'creditos': int(match[2]),
                    'requisito': match[3].strip().replace("'", ""),
                    'area': match[4].strip(),
                    'nivel': match[5].strip()
                })
        
        except Exception as e:
            print(f"Error parseando cursos.pl: {e}")
        
        return cursos
    
    def _get_cursos_disponibles_fallback(self, query: str, cursos_db: List[Dict]) -> str:
        """
        Implementación Python de cursos_disponibles
        """
        # Extraer cursos aprobados del query
        match = re.search(r'\[([^\]]+)\]', query)
        if not match:
            return "[]"
        
        aprobados_str = match.group(1)
        cursos_aprobados = [c.strip().replace("'", "") for c in aprobados_str.split(',')]
        
        # Filtrar cursos disponibles
        disponibles = []
        for curso in cursos_db:
            # No incluir si ya está aprobado
            if curso['codigo'] in cursos_aprobados:
                continue
            
            # Verificar requisito
            req = curso['requisito']
            if req == 'ninguno' or req in cursos_aprobados:
                disponibles.append(curso['codigo'])
        
        return str(disponibles)
    
    def _get_info_curso_fallback(self, query: str, cursos_db: List[Dict]) -> str:
        """
        Implementación Python de info_curso
        """
        match = re.search(r"'([^']+)'", query)
        if not match:
            return ""
        
        codigo = match.group(1)
        curso = next((c for c in cursos_db if c['codigo'] == codigo), None)
        
        if curso:
            return f"{curso['nombre']}, {curso['creditos']}, {curso['area']}, {curso['nivel']}"
        
        return ""
    
    def get_cursos_disponibles(self, cursos_aprobados: List[str]) -> List[str]:
        """
        Obtiene los cursos disponibles para matricular
        """
        # Formatear lista para Prolog
        aprobados_str = "[" + ", ".join([f"'{c}'" for c in cursos_aprobados]) + "]"
        
        query = f"cursos_disponibles(_, {aprobados_str}, Cursos), write(Cursos)"
        result = self._execute_query(query)
        
        # Parsear resultado
        if result and result != "false":
            # Extraer códigos de cursos
            codigos = re.findall(r"'([^']+)'", result)
            return codigos
        
        return []
    
    def get_info_curso(self, codigo_curso: str) -> Dict[str, Any]:
        """
        Obtiene información completa de un curso
        """
        query = f"info_curso('{codigo_curso}', Nombre, Creditos, Area, Nivel), format('~w|~w|~w|~w', [Nombre, Creditos, Area, Nivel])"
        result = self._execute_query(query)
        
        if result and result != "false":
            parts = result.split('|')
            if len(parts) == 4:
                return {
                    'codigo': codigo_curso,
                    'nombre': parts[0],
                    'creditos': int(parts[1]),
                    'area': parts[2],
                    'nivel': parts[3]
                }
        
        # Fallback: buscar en el archivo
        cursos_db = self._load_cursos_from_pl()
        curso = next((c for c in cursos_db if c['codigo'] == codigo_curso), None)
        return curso if curso else {}
    
    def get_requisito(self, codigo_curso: str) -> str:
        """
        Obtiene el requisito de un curso
        """
        cursos_db = self._load_cursos_from_pl()
        curso = next((c for c in cursos_db if c['codigo'] == codigo_curso), None)
        
        if curso:
            return curso['requisito']
        
        return "ninguno"
    
    def get_all_cursos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los cursos de la base de datos
        """
        return self._load_cursos_from_pl()

# Instancia global del servicio
prolog_service = PrologService()