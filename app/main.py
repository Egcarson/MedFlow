from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import engine
from app.routers import auth, patients

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    auth.auth_router, tags=["Authentication"])
app.include_router(patients.router)

@app.get('/')
def root():
    return {'message': 'Hello, World!'}
