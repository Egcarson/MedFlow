from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schema, oauth2
from app.crud.patients import patient_crud_service
from app.crud.appointment import get_uncompleted_appointments
from app.crud.emr import emr_crud_service
from app.database import get_db
from app.oauth2 import get_current_user


router = APIRouter(
    tags=['Emr']
)


@router.get('/emr/{patient_id}', status_code=200)
async def get_patient_record(patient_id: int, db: Session = Depends(get_db), patient_current_user: models.Patient = Depends(oauth2.get_current_user), doctor_current_user: models.Doctor = Depends(oauth2.get_current_user)):
    patient = patient_crud_service.get_patient_by_id(id=patient_id, db=db)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Emr with patient id not found')
    if patient_current_user.id != patient_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Patient not authorized to view records')
    

    # This logic is just to make sure that only doctors with uncompleted appointments with patient can check the record
    appointments = get_uncompleted_appointments(patient_id=patient_id, db=db)

    doctors_id = [appointment.doctor_id for appointment in appointments]

    if doctor_current_user.id not in doctors_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Doctor not authorized to view records')
    
    Emr = emr_crud_service.get_patient_EMR(db, patient_id=patient_id)

    if not Emr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No record for this patient')
    
    return Emr

@router.post('/emr/{patient_id}', status_code=201)
async def create_record(patient_id: int,  payload: schema.EMRCreate, db: Session = Depends(get_db), current_user: schema.Patient = Depends(get_current_user)):
    patient = patient_crud_service.get_patient_by_id(patient_id, db)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Patient not found')
    
    if patient.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authorized')
    
    Emr = emr_crud_service.create_patient_EMR(db, payload)

    return Emr


@router.delete('/emr', status_code=200)
async def delete_record(patient_id: int, db: Session = Depends(get_db), current_user: schema.Patient = Depends(get_current_user)):
    emr = emr_crud_service.get_patient_EMR(
        db, patient_id)
    if not emr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Record not found')

    if patient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authorized')

    emr = emr_crud_service.delete_patient_EMR(db, patient_id)

    return {'message': 'Record deleted successfully'}
