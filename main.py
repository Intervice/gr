# main.py
from fastapi import FastAPI
from src.database.db import engine
from src.database.models import Base

Base.metadata.create_all(bind=engine)

from src.routes import skills

app = FastAPI(title="SkillSwap API",
              description="Desc",
              version="1.0.0")

app.include_router(skills.router)

@app.get("/health")
def read_root():
    return {"message": "test main root"}
