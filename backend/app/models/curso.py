from pydantic import BaseModel
from typing import List, Optional

class Curso(BaseModel):
    codigo: str
    nombre: str
    creditos: int
    requisito: Optional[str] = None
    area: str
    nivel: str

class CursoHistorial(BaseModel):
    curso: str
    estado: str  # 'aprobado', 'en-curso', 'pendiente'
    calificacion: Optional[int] = None
    periodo: Optional[str] = None

class Recomendacion(BaseModel):
    codigo: str
    nombre: str
    creditos: int
    nivel: str
    analisisProlog: List[str]
    explicacionIA: str