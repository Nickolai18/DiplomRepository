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

secret_key = "gV64m9aIzFG4qpgVphvQbPQrtAO0nM-7YwwOvu0XPt5KJOjAy4AfgLkqJXYEt"
algoritm = "HS256"

SQLALCHEMY_DATABASE_URL = "mysql://root:root@127.0.0.1:3306/calls"
engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

class Base(DeclarativeBase): pass

class Calls(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    employee = Column(String, default='')
    secondary_employee = Column(String, default='')
    critical = Column(Integer)
    time_to_complete = Column(Integer)
    status = Column(Integer)
    # sla = relationship("SLA", uselist=False, back_populates="ticket")

    def deserialzator(self):
        des = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "employee": self.employee,
            "employee": self.employee,
            "secondary_employee": self.secondary_employee,
            "critical": self.critical,
        }
        return des
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    role = Column(String)
    login = Column(String)
    password = Column(String)

    def deserialzator(self):
        des = {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "role": self.role,
        }
        return des

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String)
    number_of_calls = Column(Integer)
    current_calls = Column(Integer)
    id_users = Column(Integer)

    def deserialzator(self):
        des = {
            "id_users": self.id_users,
            "code": self.code,
            "number_of_calls": self.number_of_calls,
            "current_calls": self.current_calls,
            "id_users": self.id_users
        }
        return des

class SLA(Base):
    __tablename__ = "sla"

    idSLA = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(DateTime)
    confirm_date = Column(DateTime)
    add_another_employee = Column(DateTime)
    add_new_employee = Column(DateTime)
    id_ticket = Column(DateTime, ForeignKey("calls.id"))
    # ticket = relationship("User", back_populates="sla")

    def deserialzator(self):
        des = {
            "create_date": self.create_date,
            "confirm_date": self.confirm_date,
            "add_another_employee": self.add_another_employee,
            "add_new_employee": self.add_new_employee,
        }
        return des

class BaseId(BaseModel):
    id: int | None
    employee: str | None
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))

def create_code(name: str, surname: str):
    eng_name = translit(name, 'ru', reversed=True)
    eng_surname = translit(surname, 'ru', reversed=True)
    code = eng_name[0] + eng_surname[0]
    return code

def authenticate_user(login, password):
    user = db.query(User).filter(User.login == login).first()
    if not user or verify_password(plain_password=password, hashed_password=user.password) == 0:
        return None
    return user

def get_current_user(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        return None
    payload = jwt.decode(token, secret_key, algorithms=algoritm)
    role_id = payload.get('role')
    return role_id

# @app.get("/me")
# def get_me(users_access_token = Cookie(None)):
#     tok = get_current_user(users_access_token)
#     return {"users_access_token": tok}

@app.get("/login")
def render_main_index():
    return FileResponse("static/login.html")
 
@app.post("/login")
def auth_user(request: Request, response: Response, login = Form(), password = Form(), token = Depends(get_current_user)):
    user = authenticate_user(login, password)
    # print(user.role)N
    access_token = create_access_token(secret_key, algoritm, {"role": str(user.role)})
    redirect_op = RedirectResponse("/redirect", status_code=303)
    redirect_op.set_cookie(key='access_token', value=access_token, httponly=True)
    # if token == "operator":
    #     return redirect_op
    # if token == "admin":
    #     return redirect_ad
    # if token == None:
    return redirect_op

@app.get("/redirect")
def login_user(token = Depends(get_current_user)):
    redirect_op = RedirectResponse("/", status_code=303)
    redirect_ad = RedirectResponse("/create_user", status_code=303)
    redirect = RedirectResponse("/login", status_code=303)
    if token == "operator":
        return redirect_op
    if token == "admin":
        return redirect_ad
    if token == None:
        return redirect

@app.get("/create_user")
def render_main_index():
    return FileResponse("static/create_user.html")


@app.post("/create_user")
def register_user(name = Form(), surname = Form(), login = Form(), password = Form(), role = Form()):
    last_user = db.query(User)
    arr = []
    for elem in last_user:
        arr.append(elem.deserialzator())
    last_user = arr[-1]
    new_user = User(id = last_user["id"] + 1, login = login, password = get_password_hash(password), role = role, name = name, surname = surname)
    db.add(new_user)
    try:
        db.commit()
    except:
        db.rollback()
        raise
    if role == "employee":
        new_employee = Employee(code=create_code(name, surname), number_of_calls = 0, current_calls = 0, id_users = new_user.id)
        db.add(new_employee)
    try:
        db.commit()
    except:
        db.rollback()
        raise
    return FileResponse("static/create_user.html")



def countAvg(start, cancel):
    delta = cancel - start
    return delta.total_seconds() / 3600

def getAllUser():
    usersUndes = db.query(User).filter(User.role=='employee')
    users = []
    for user in usersUndes:
        usersEmplo = db.query(Employee).filter(Employee.id_users == user.id).first()
        user = user.deserialzator()
        user.update(
            {
                'current_calls': usersEmplo.current_calls,
                'code': usersEmplo.code,
            }
        )
        users.append(user)
    for user in users:
        print(user)
    return users
# us = getAllUser()
# for elem in us:
#     print(elem)
def getEmployee():
    usersUndes = db.query(Employee)
    users = []
    for user in usersUndes:
        usersEmplo = db.query(User).filter(User.id == user.id_users).first()
        user = user.deserialzator()
        user.update(
            {
                'name': usersEmplo.name
            }
        )
        users.append(user)
    for user in users:
        print(user)
    return users
# getEmployee()
#     usersUndes = db.query(User).filter(User.role=='employee')
#     usersEmployee = db.query(Employee)
#     users = []
#     usersEmployeeFetch = []
#     for user in usersUndes:
#         users.append(user.deserialzator())
#     for user in usersEmployee:
#         usersEmployeeFetch.append(user.deserialzator())
#     for i in range(len(users)):
#         users[i].update('current_calls': usersEmployeeFetch[i]['current_user'])
#     for user in users:
#         print(user)
#     return users

# Загрузка главной проблемы(страницы)
@app.get("/")
def render_main_index(response: Response):
    # response.set_cookie(key="users_acc", value='rrr', httponly=True)
    # role = token
    # if role == "operator":
    #     return FileResponse("static/index.html")
    # if role == "admin":
    #     return FileResponse("static/create_login.html")
    # if role == None:
    #     return FileResponse("static/login.html")
    return FileResponse("static/index.html")




# Загрузка страницы с актуальными заявками
@app.get("/tickets")
def render_tickets():
    return FileResponse("static/tickets.html")

@app.get("/analise")
def render_average():
    return FileResponse("static/analise.html")

@app.get("/api/users")
def get_users():
    return getAllUser()

@app.get("/api/employee")
def get_users():
    return getEmployee()


@app.get("/api/cards")
def render_main_page():
    ol = db.query(Calls)
    arrOfTest = []
    for elem in ol:
        print(elem.deserialzator())
        calls = elem.deserialzator()
        # print(calls["employee"])
        print(calls["secondary_employee"])
        # if (calls["employee"] == "" and calls["secondary_employee"] == None) or (calls["employee"] != "" or calls["secondary_employee"] == ""):
        if calls["employee"] == "" or calls["secondary_employee"] == '':
            if wordValidation(calls["description"]):
                arrOfTest.append(elem.deserialzator())
    return arrOfTest



@app.get("/api/tickets")
def render_tickets_page():
    ol = db.query(Calls).filter(Calls.status == 0)
    # now = datetime.now()
    arrOfTest = []
    for elem in ol:
        calls = elem.deserialzator()
        sla = db.query(SLA).filter(SLA.id_ticket == calls["id"]).first()
        print(sla.deserialzator())
        print(calls)
        if (calls["employee"] != "" and calls["secondary_employee"] == None) or (calls["employee"] != "" and calls["secondary_employee"] != ""):
            arrOfTest.append(elem.deserialzator())
        else:
            print(2)
        if sla.confirm_date != None:
            print("second")
            # if sla.create_date != None:
            #     sla.create_calls = now.strftime("%Y-%m-%d %H:%M:%S")
            delta = sla.confirm_date - sla.create_date
            delta = int(delta.days)
        else:
            print("firsyt")
            delta = 0
        print(sla.create_date)
        # print(sla.confirm_date)
        print(delta)
        print(elem.deserialzator())
        print(calls["employee"])
        if calls["critical"] == 0 and delta > 3:
            calls["critical"] = 1
            arrOfTest.append(calls)
        if calls["critical"] == 1 and delta > 7:
            callCriticalLevel2 = db.query(Calls).filter(Calls.id == calls["id"]).first()
            callCriticalLevel2.critical = callCriticalLevel2.critical + 1
            callCriticalLevel2.employee = ""
            db.commit()
    print(1)
    print(arrOfTest)
    return arrOfTest

@app.get("/api/average")
def average():
    sla = db.query(SLA)
    arrSla = []
    arrAvgSla = []
    confirm_date = 0
    add_another_employee = 0
    add_new_employee = 0
    for elem in sla:
        arrSla.append(elem.deserialzator())
    for elem in arrSla:
         if elem["confirm_date"] != None:
             confirm_date += countAvg(elem["create_date"], elem["confirm_date"])
         else:
            confirm_date += 0
         if elem["add_another_employee"] != None:
             add_another_employee += countAvg(elem["create_date"], elem["add_another_employee"])
         else:
             add_another_employee += 0
         if elem["add_new_employee"] != None:
             add_new_employee += countAvg(elem["create_date"], elem["add_new_employee"])
         else:
             add_new_employee += 0

    print(confirm_date)
    print(add_another_employee)
    print(add_new_employee)
    arrAvgSla.append(round(confirm_date / len(arrSla), 1))
    arrAvgSla.append(round(add_another_employee / len(arrSla), 1))
    arrAvgSla.append(round(add_new_employee / len(arrSla), 1))
    print(arrAvgSla)
    return arrAvgSla




@app.post("/")
def form(id = Form(), employee = Form()):
    now = datetime.now()
    nowMySQL = now.strftime("%Y-%m-%d %H:%M:%S")
    call = db.query(Calls).filter(Calls.id == id).first()
    secondary_employee = call.secondary_employee
    if secondary_employee == None:
        print("first")
        if employee == 'auto':
            # print(employee)
            usersTo = getAllUser()
            smallestTicket = 100000000
            userCodeSmallest = ''
            for user in usersTo:
                employee = db.query(Employee).filter(Employee.id_users == user['id']).first()
                print(employee.deserialzator())
                employee = employee.deserialzator()
                print(1)
                print(employee['current_calls'])
                if employee['current_calls'] < smallestTicket:
                    smallestTicket = employee['current_calls']
                    userCodeSmallest = employee['code']
            print(userCodeSmallest)
            user = db.query(Employee).filter(Employee.code == userCodeSmallest).first()
            user.number_of_calls = user.number_of_calls + 1
            user.current_calls = user.current_calls + 1
            employee = userCodeSmallest
        else:
            user = db.query(Employee).filter(Employee.code == employee).first()
            user.number_of_calls = user.number_of_calls + 1
            user.current_calls = user.current_calls + 1
        sla = db.query(SLA).filter(SLA.id_ticket == id).first()
        print(sla.deserialzator())
        call.employee = employee
        if sla.confirm_date != '':
            sla.add_new_employee = nowMySQL
        else:
            sla.confirm_date = nowMySQL
        call.time_to_complete = 3
    elif secondary_employee == '':
        print("second")
        if employee == 'auto':
            print(employee)
            usersTo = getAllUser()
            print(usersTo)
            smallestTicket = 100000000
            userCodeSmallest = ''
            for user in usersTo:
                if user["current_calls"] < smallestTicket:
                    smallestTicket = user["current_calls"]
                    userCodeSmallest = user["code"]
            print(userCodeSmallest)
            user = db.query(Employee).filter(Employee.code == userCodeSmallest).first()
            user.number_of_calls = user.number_of_calls + 1
            user.current_calls = user.current_calls + 1
            employee = userCodeSmallest
        else:
            user = db.query(Employee).filter(Employee.code == employee).first()
            print(user.deserialzator())
            user.number_of_calls = user.number_of_calls + 1
            user.current_calls = user.current_calls + 1
        sla = db.query(SLA).filter(SLA.id_ticket == id).first()
        call.secondary_employee = employee
        if sla.confirm_date != '':
            sla.add_another_employee = nowMySQL
        else:
            sla.confirm_date = nowMySQL
        call.time_to_complete = 7
    db.commit()
    return FileResponse("static/index.html")

# Изменить сотрудника
@app.post("/tickets")
def form_tickets(id = Form()):
    # Записывает текущее время в переменную
    now = datetime.now()
    # Вытягивание соответствующих строк
    call = db.query(Calls).filter(Calls.id == id).first()
    user = db.query(Employee).filter(Employee.code == call.employee).first()
    # Измениние соответствующих строк
    user.current_calls -= 1
    if call.secondary_employee == None:
        call.employee = ''
    else:
        call.employee = call.secondary_employee
        call.secondary_employee = None
    # Сохранение соответствующих строк
    try:
        db.commit()
    except:
        db.rollback()
        raise
    # Возвращение на страницу
    return FileResponse("static/tickets.html")

# Добавить дополнительного сотрудника
@app.post("/tickets/addnewuser")
def form_add_new_user(id = Form()):
    # Записывает текущее время в переменную
    now = datetime.now()
    # Вытягивание соответствующих строк
    call = db.query(Calls).filter(Calls.id == id).first()
    # Измениние соответствующих строк
    call.secondary_employee = ''
    # Сохранение соответствующих строк
    db.commit()
    return FileResponse("static/tickets.html")

@app.post("/complete_tickets")
def change_status(id = Form()):
    call = db.query(Calls).filter(Calls.id == id).first()
    call.status = 1
    try:
        db.commit()
    except:
        db.rollback()
        raise
    return FileResponse("static/tickets.html")
