from typing import Annotated

from fastapi import FastAPI, Form, Body, HTTPException, Response, Request, Cookie, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, desc
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from bd import SessionLocal
from datetime import datetime
from jose import jwt, JWTError
from transliterate import translit

from validation import wordValidation

from auth import get_password_hash, verify_password, create_access_token
app = FastAPI()

secret_key = "gV64m9aIzFG4qpgVphvQbPQrtAO0nM-7YwwOvu0XPt5KJOjAy4AfgLkqJXYEt"
algoritm = "HS256"

@app.get("/")
def render_main_index():
    return FileResponse("static/login.html")


@app.post("/login")
def auth_user(request: Request, response: Response, login = Form(), password = Form()):
    access_token = create_access_token(secret_key, algoritm, {"role": 'rrrrr'})
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    # if role == "operator":
    #     return FileResponse("static/index.html")
    # if role == "admin":
    #     return FileResponse("static/create_user.html")
    # if role == None:
    #     return FileResponse("static/login.html")
    return {'token': access_token, 'login': login, 'password': password}

