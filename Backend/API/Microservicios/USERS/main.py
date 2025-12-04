from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["Proyecto"]
users_collection = db["Users"]


@app.post("/login/{user}/{password}")
def loginAPI(user: str, password: str):
    resultado = login(user, password)
    if resultado:
        return {"status": "success", "message": "Login correcto"}
    else:
        return {"status": "error", "message": "Credenciales incorrectas"}


@app.put("/register/{user}/{password}")
def registerAPI(user: str, password: str):
    resultado = register(user, password)
    if resultado:
        return {"status": "success", "message": "Registro correcto"}
    else:
        return {"status": "error", "message": "Hubo un error en el registro"}

def login(user, password):
    usuario = users_collection.find_one({
        "userName": user,
        "passwordUser": password
    })

    return usuario is not None


def register(user, password):

    existe = users_collection.find_one({"userName": user})
    if existe:
        return False

    users_collection.insert_one({
        "userName": user,
        "passwordUser": password
    })

    return True