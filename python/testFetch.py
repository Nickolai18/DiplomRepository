from fastapi import FastAPI, Form, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from bd import SessionLocal

class BaseId(BaseModel):
    id: int | None
    employee: str | None

app = FastAPI()

@app.post("/test")
def fetch(base: BaseId):
    return {"message": f"Привет, {base.employee}, твой возраст - {base.id}"}