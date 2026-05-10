from fastapi import FastAPI, Form, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from bd import SessionLocal
from datetime import datetime

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
    create_date = Column(DateTime)
    confirm_date = Column(DateTime)
    def deserialzator(self):
        des = {
            "id": self.id,
            "title":self.title,
            "description":self.description,
            "employee":self.employee
        }
        return des
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    code = Column(String)
    number_of_calls = Column(Integer)

    def deserialzator(self):
        des = {
            "name": self.name,
            "surname": self.surname,
            "code": self.code,
            "number_of_calls": self.number_of_calls
        }
        return des
class BaseId(BaseModel):
    id: int | None
    employee: str | None
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))

@app.get("/api/users")
def get_users():
    usersUndes = db.query(User)
    users = []
    for user in usersUndes:
        # print(user.deserialzator())
        users.append(user.deserialzator())
    for user in users:
        print(user)
    return users

@app.get("/api/cards")
def render_main_page():
    ol = db.query(Calls)
    arrOfTest = []
    for elem in ol:
        # print(f"{elem.id} {elem.title}-{elem.description}")
        # print(elem.deserialzator())
        print(elem.deserialzator())
        calls = elem.deserialzator()
        print(calls["employee"])
        if calls["employee"] == "":
            arrOfTest.append(elem.deserialzator())
    # for test in ol:
    #     return test.deserialzator()
    # test1 = db.query(Task).filter(Task.id ==1).first()
    return arrOfTest
@app.get("/")
def render_main_index():
    return FileResponse("static/index.html")
@app.get("/item")
def item():
    return {"message":"hh"}
@app.get("/fetch")
def test():
    return {
        "message":{
            "id":1,
            "title":"test",
            "description":"test",
            "isComplete":"0",
        },
    }
# new_test_user = User(id = 1, name="Николай", surname="Ротарь", code="hr", number_of_calls=0)
# db.add(new_test_user)
# db.commit()
# def redir():
#     @app.get("/")
#     def resp():
#         return RedirectResponse("/")
#     return resp
@app.post("/")
def form(id = Form(), employee = Form()):
    # new_task = Task(id=14,title="New69", description=f"{employee}", employee="ru")
    # db.add(new_task)
    # db.commit()
    # for elem in ol:
    #     print(f"{elem.id} {elem.title}-{elem.description}")
    now = datetime.now()
    nowMySQL = now.strftime("%Y-%m-%d %H:%M:%S")
    call = db.query(Calls).filter(Calls.id == id).first()
    call.employee = employee
    call.confirm_date = nowMySQL
    db.commit()
    return FileResponse("static/index.html")
    # @app.get("/")
    # def resp():
    #     return RedirectResponse("/")
    # return resp()

# @app.get("/test")


# def fetch(base: BaseId):
#     return {"message": f"Привет, {base.employee}, твой возраст - {base.id}"}


# @app.post("/test1")
# def fetch(base: BaseId):
#     return {"message": f"Привет, {base.employee}, твой возраст - {base.id}"}

now = datetime.now()
# nowMySQL = now.strftime("%Y-%m-%d %H:%M:%S")
# dateCalls = Calls(id=4, title="New70", description="Not NEWWW", create_date=nowMySQL)
# db.add(dateCalls)
# db.commit()