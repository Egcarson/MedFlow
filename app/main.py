from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import engine
from app.routers.auth import auth_router
from app.routers.doctors import doctor_router

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    auth_router, prefix="/", tags=["Authentication"])
app.include_router(doctor_router, prefix='/doctors', tags=['Doctors'])

@app.get('/')
def root():
    return {'message': 'Hello, World!'}
