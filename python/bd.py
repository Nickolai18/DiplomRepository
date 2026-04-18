from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, bind=engine)

db = SessionLocal()

class Base(DeclarativeBase): pass

class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    emploer = Column(String, default="")


Base.metadata.create_all(bind=engine)

pc1 = Call(title="PC1", description="Pdfgssdgslu dsiuf j jhhhfdsg")
pc2 = Call(title="PC2", description="Pdfgssdgs j jhhhfdsg")
pc3 = Call(title="PC3", description="Pdfgssdgsdfdghlu dsiuf uy jhhhfdsg")
db.add_all([pc1, pc2, pc3])
db.commit()

app=FastAPI()