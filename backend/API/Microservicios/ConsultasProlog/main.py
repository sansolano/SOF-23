from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from pyswip import Prolog
from ollama import Client

app = FastAPI()
client = Client()

# Inicializar Prolog
prolog = Prolog()
prolog.consult("cursos.pl")

class CursosInput(BaseModel):
    username: str
    cursos_aprobados: List[str]

@app.post("/cursos/recomendados")
def cursos_recomendados(data: CursosInput):

    # Convertir lista de cursos aprobados a formato Prolog
    aprobados_str = "[" + ",".join(data.cursos_aprobados) + "]"
    query = f"cursos_disponibles_nombre({aprobados_str}, NombresCursos)"
    resultado = list(prolog.query(query))

    cursos_disponibles = []
    if resultado:
        cursos_disponibles = [str(c) for c in resultado[0]["NombresCursos"]]

    prompt = f"""
    Eres un asesor académico. Un estudiante llamado {data.username} tiene los siguientes cursos aprobados: {data.cursos_aprobados}.
    Los cursos disponibles para él son: {cursos_disponibles}.
    Explica brevemente por qué debería matricularlos.
    """

    response = client.chat(
    model="llama2",
    messages=[{"role": "user", "content": prompt}]
)

    # ✅ forma segura de obtener el texto
    recomendacion = response["message"]["content"] if "message" in response else response.get("content", "")

    return {
        "status": "success",
        "cursos_disponibles": cursos_disponibles,
        "recomendacion": recomendacion
    }