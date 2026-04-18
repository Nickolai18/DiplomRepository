from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from numpy.f2py.auxfuncs import iscomplex
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from fastapi.responses import RedirectResponse
from bd import SessionLocal

SQLALCHEMY_DATABASE_URL = "mysql://root:root@127.0.0.1:3306/tasks"
engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

class Base(DeclarativeBase): pass

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    employee = Column(String)

    def deserialzator(self):
        des = {
            "title":self.title,
            "description":self.description,
            "employee":self.employee
        }
        return des
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    task = Column(Integer)

    def deserialzator(self):
        des = {
            "name": self.name,
            "code": self.code,
            "task": self.task
        }
        return des
ol = db.query(Task)
usersUndes = db.query(User)
users = []
arrOfTest = []
hh = {"jj":"hjghghg"}
for elem in ol:
    # print(f"{elem.id} {elem.title}-{elem.description}")
    # print(elem.deserialzator())
    arrOfTest.append(elem.deserialzator())
for user in usersUndes:
    # print(user.deserialzator())
    users.append(user.deserialzator())
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))

@app.get("/api/users")
def get_users():
    for user in users:
        print(user)
    return users
@app.get("/api/tasks")
def render_main_page():
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
@app.post("/postdata")
def form(country = Form()):
    new_task = Task(id=14,title="New69", description=f"{country}", employee="ru")
    db.add(new_task)
    db.commit()
    for elem in ol:
        print(f"{elem.id} {elem.title}-{elem.description}")
    return RedirectResponse("/", status_code=301)
