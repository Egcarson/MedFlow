

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.oauth2 import authenticate_user, create_access_token, pwd_context
from app.database import get_db
from app import schema
from app.crud.patients import patient_crud_service
from app.crud.doctors import doctor_crud_service
from app.utils import validate_password 

auth_router = APIRouter()


@auth_router.post('/signup/patient', status_code=201, response_model=schema.Patient)
async def create_patient(payload: schema.PatientCreate, db: Session = Depends(get_db)):
    patient = patient_crud_service.get_patient(db, credential=payload.email)
    if patient:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already registered')
    patient = patient_crud_service.get_patient(db, credential=payload.hospital_card_id)
    if patient:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Hospital ID already registered')
    
    # Validate password
    password_validation_result = validate_password(
        payload.password, payload.first_name, payload.last_name)

    if password_validation_result != "Password is valid":
        raise HTTPException(status_code=400, detail=password_validation_result)
    
    hashed_password = pwd_context.hash(payload.password)
    payload.password = hashed_password
    return patient_crud_service.create_patient(db=db, payload=payload)


@auth_router.post('/signup/doctor', status_code=201, response_model=schema.Doctor)
async def create_doctor(payload: schema.DoctorCreate, db: Session = Depends(get_db)):
    doctor = doctor_crud_service.get_doctor(db, credential=payload.email)
    if doctor:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Email already registered')
    doctor = doctor_crud_service.get_doctor(
        db, credential=payload.hospital_id)
    if doctor:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Hospital ID already registered')

    # Validate password
    password_validation_result = validate_password(
        payload.password, payload.first_name, payload.last_name)

    if password_validation_result != "Password is valid":
        raise HTTPException(status_code=400, detail=password_validation_result)

    hashed_password = pwd_context.hash(payload.password)
    payload.password = hashed_password

    return doctor_crud_service.create_doctor(db=db, payload=payload)


@auth_router.post("/login", status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, credential=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
