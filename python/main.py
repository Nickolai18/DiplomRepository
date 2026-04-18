from fastapi import FastAPI, Body
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

# app.mount("/", StaticFiles(directory="static", html=True))
# @app.get("/")
# def render():
#     return FileResponse("static/index.html")
@app.post("/hello")
def hello(data = Body()):
    emplo = data["emploer"]
    return {"message": f"Привет {emplo}"}
# @app.get("/")
# def index():
#     return {"message": "Привет, МИР!"}
#
# @app.get("/items/{item_id}")
# def task(item_id: int):
#     return {"item_id": item_id, "name": f"Задача номер {item_id}"}