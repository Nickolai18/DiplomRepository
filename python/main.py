from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Привет, МИР!"}

@app.get("/items/{item_id}")
def task(item_id: int):
    return {"item_id": item_id, "name": f"Задача номер {item_id}"}