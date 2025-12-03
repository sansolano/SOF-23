from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from pyswip import Prolog

app = FastAPI()
prolog = Prolog()
prolog.consult("../ConsultasProlog/cursos.pl")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class CursosInput(BaseModel):
    username: str
    cursos_aprobados: List[str]
    
client = MongoClient("mongodb://localhost:27017/")
db = client["Proyecto"]
users_collection = db["Cursos"]

class CourseList(BaseModel):
    cursos: List[str]


@app.post("/user/course/add/{username}")
def add_courses(username: str, data: CourseList):

    result = users_collection.update_one(
        {"userName": username},
        {
            "$set": {
                "userName": username,
                "cursos": data.cursos
            }
        },
        upsert=True
    )

    if result.matched_count == 1:
        return {"status": "success", "message": "Cursos actualizados correctamente"}

    if result.upserted_id is not None:
        return {"status": "success", "message": "Usuario creado y cursos guardados"}

    return {"status": "error", "message": "Error inesperado"}


@app.get("/user/course/{username}")
def get_courses(username: str):

    user = users_collection.find_one(
        {"userName": username},
        {"_id": 0, "cursos": 1, "userName": 1}
    )

    if not user:
        return {"status": "error", "message": "Usuario no encontrado"}

    return {
        "status": "success",
        "userName": user["userName"],
        "cursos": user.get("cursos", [])
    }
    
