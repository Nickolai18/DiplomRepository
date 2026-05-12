from fastapi import FastAPI, Form, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from bd import SessionLocal
from datetime import datetime

from validation import wordValidation

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
    code = Column(String)
    number_of_calls = Column(Integer)
    current_calls = Column(Integer)

    def deserialzator(self):
        des = {
            "name": self.name,
            "surname": self.surname,
            "code": self.code,
            "number_of_calls": self.number_of_calls,
            "current_calls": self.current_calls
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

def getAllUser():
    usersUndes = db.query(User)
    users = []
    for user in usersUndes:
        users.append(user.deserialzator())
    for user in users:
        print(user)
    return users

# Загрузка главной проблемы(страницы)
@app.get("/")
def render_main_index():
    return FileResponse("static/index.html")

# Загрузка страницы с актуальными заявками
@app.get("/tickets")
def render_tickets():
    return FileResponse("static/tickets.html")

@app.get("/api/users")
def get_users():
    return getAllUser()

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
    ol = db.query(Calls)
    arrOfTest = []
    for elem in ol:
        calls = elem.deserialzator()
        sla = db.query(SLA).filter(SLA.id_ticket == calls["id"]).first()
        delta = sla.confirm_date - sla.create_date
        # print(sla["create_date"])
        # print(sla["confirm_date"])
        print(delta.days)
        delta = int(delta.days)
        print(elem.deserialzator())
        print(calls["employee"])
        if (calls["employee"] != "" and calls["secondary_employee"] == None) or (calls["employee"] != "" and calls["secondary_employee"] != ""):
            arrOfTest.append(elem.deserialzator())
        if calls["critical"] == 0 and delta > 3:
            calls["critical"] = 1
            arrOfTest.append(calls)
        if calls["critical"] == 1 and delta > 7:
            callCriticalLevel2 = db.query(Calls).filter(Calls.id == calls["id"]).first()
            callCriticalLevel2.critical = callCriticalLevel2.critical + 1
            callCriticalLevel2.employee = ""
            db.commit()

    return arrOfTest



@app.post("/")
def form(id = Form(), employee = Form()):
    now = datetime.now()
    nowMySQL = now.strftime("%Y-%m-%d %H:%M:%S")
    call = db.query(Calls).filter(Calls.id == id).first()
    secondary_employee = call.secondary_employee
    if secondary_employee == None:
        if employee == 'auto':
            print(employee)
            usersTo = getAllUser()
            smallestTicket = 100000000
            userCodeSmallest = ''
            for user in usersTo:
                if user["current_calls"] < smallestTicket:
                    smallestTicket = user["current_calls"]
                    userCodeSmallest = user["code"]
            print(userCodeSmallest)
            user = db.query(User).filter(User.code == userCodeSmallest).first()
            user.number_of_calls = user.number_of_calls + 1
            user.current_calls = user.current_calls + 1
            employee = userCodeSmallest
        else:
            user = db.query(User).filter(User.code == employee).first()
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
        if employee == 'auto':
            print(employee)
            usersTo = getAllUser()
            smallestTicket = 100000000
            userCodeSmallest = ''
            for user in usersTo:
                if user["current_calls"] < smallestTicket:
                    smallestTicket = user["current_calls"]
                    userCodeSmallest = user["code"]
            print(userCodeSmallest)
            user = db.query(User).filter(User.code == userCodeSmallest).first()
            user.number_of_calls = user.number_of_calls + 1
            user.current_calls = user.current_calls + 1
            employee = userCodeSmallest
        else:
            user = db.query(User).filter(User.code == employee).first()
            user.number_of_calls = user.number_of_calls + 1
            user.current_calls = user.current_calls + 1
        sla = db.query(SLA).filter(SLA.id_ticket == id).first()
        call.employee = employee
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
    user = db.query(User).filter(User.code == call.employee).first()
    # Измениние соответствующих строк
    user.current_calls -= 1
    call.employee = ''
    # Сохранение соответствующих строк
    db.commit()
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

