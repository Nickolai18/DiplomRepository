from fastapi import FastAPI, Form, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from bd import SessionLocal

# class BaseId(BaseModel):
#     id: int | None
#     employee: str | None

app = FastAPI()

@app.get("/items/?skip={id}&limit={emplo}")
async def read_item(id: int, emplo: str):
    return {"message": f"Привет, {id}, твой возраст - {emplo}"}

@app.post("/tt")
def fetch(id = Body(embed=True),emplo = Body(embed=True)):
# def fetch(data = Body()):
    return {"message": f"Привет, {id}, твой возраст - {emplo}"}