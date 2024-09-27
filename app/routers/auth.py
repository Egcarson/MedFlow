

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.oauth2 import authenticate_user, create_access_token, pwd_context, verify_password
from app.database import get_db
from app import schema, models,oauth2
from app.crud.patients import patient_crud_service
from app.crud.doctors import doctor_crud_service
from app.crud import appointment as apt_crud
from app.utils import validate_password, users_email, update_password, users_id

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

@auth_router.post('/auth/password_reset', status_code=status.HTTP_202_ACCEPTED)
def password_reset(payload: schema.PasswordReset, db: Session = Depends(get_db), patient_current_user: models.Patient=Depends(oauth2.get_current_user), doctor_current_user: models.Doctor=Depends(oauth2.get_current_user)):
    user = users_email(email=payload.email, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email you supplied does not exist."
        )
    
    #validate user
    patient_user = users_id(patient_current_user.id, db)
    doctor_user = users_id(doctor_current_user.id, db)
    if patient_user.email != user.email and doctor_user.email != user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not allowed to perform this action!"
        )
    
    
    if payload.new_password != payload.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password does not match!"
        )
    
    password_check = validate_password(payload.new_password, user.first_name, user.last_name)
    if password_check != "Password is valid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=password_check
        )
    
    if verify_password(payload.new_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too weak. Similar to old password"
        )
    
    
    update_password(payload, db)
    return {"details": "Password has been changed successfully!"}

@auth_router.put('/admin/apppointment_status', status_code=status.HTTP_202_ACCEPTED)
def appointment_status_switch(patient_id: int, appointment_id: int, payload: schema.AppointmentStatusSwitch, db: Session = Depends(get_db), current_user: models.Doctor = Depends(oauth2.get_current_user)):
    
    appointment = apt_crud.status_validation(patient_id, appointment_id, db)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient does not exist or no appointment record found for the specified patient."
        )
    
    doctor = doctor_crud_service.get_doctor_by_id(db=db, doctor_id=current_user.id)

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action!"
        )
    
    if appointment.status == schema.AppointmentStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment has already been completed! Request aborted."
        )
    
    if appointment.status == schema.AppointmentStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment has already been cancelled! Request aborted."
        )
    
    apt_crud.switch_status(patient_id, appointment_id, payload, db)
    
    return {"message": "Patient appointment status has been updated successfully"}
