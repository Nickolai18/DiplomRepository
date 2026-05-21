from fastapi import FastAPI, Form, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from bd import SessionLocal
from datetime import datetime
from auth import get_password_hash
app = FastAPI()

secret_key = "gV64m9aIzFG4qpgVphvQbPQrtAO0nM-7YwwOvu0XPt5KJOjAy4AfgLkqJXYEt"
algoritm = "HS256"

@app.get("/login")
def render_main_index():
    return FileResponse("static/create_user.html")

@app.post("/login")
def register_user(login = Form(), password = Form(), role = Form()):
    return {"login":login,"password":get_password_hash(password),"role":role}
