from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.crud.patients import patient_crud_service as pat_crud
from app.crud import appointment as apt_crud
from app import schema, database, models, oauth2

router = APIRouter(
    tags=['Appointments']
    )

@router.post('/appoointments', status_code=status.HTTP_201_CREATED, response_model=schema.Appointment)
def create_appointment(payload: schema.AppointmentCreate, patient_id: int, doctor_id: int, db: Session = Depends(database.get_db), current_user: models.Patient = Depends(oauth2.get_current_user)):
    patient = pat_crud.get_patient_by_id(patient_id, db)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The patient with id '%s' does not exist" % patient_id
        )
    
    #updating this session with doctor id validation
    # doctor = doc_crud.get_doctor_by_id(doctor_id, db)

    # validate doctor status
    # waiting for doctor endpoint

    # validating availability of doctor in the database
    # if not doctor:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="The doctor with id '%s' does not exist" % doctor_id
    #     )

    appointment = apt_crud.create_appointment(payload, patient_id, doctor_id, db)
    return appointment

@router.get('/appointments/{patient_id}', status_code=status.HTTP_200_OK, response_model=List[schema.Appointment])
def get_appointments(patient_id: int, db: Session = Depends(database.get_db), current_user: models.Patient = Depends(oauth2.get_current_user)):
    patient = pat_crud.get_patient_by_id(patient_id, db)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The patient with id '%s' does not exist" % patient_id
        )
    
    appointments = apt_crud.get_appointments_by_patient_id(patient_id, db)

    if appointments is None:
        return [{"You do not have an appointment yet."}]
    
    return appointments

@router.get('appointments', status_code=status.HTTP_200_OK, response_model=schema.Appointment)
def get_appointments(offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    appointments = apt_crud.get_appointment(offset, limit, db)
    return appointments

@router.put('/appointments/{appointment_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schema.Appointment)
def update_appointment(appointment_id: int, payload: schema.AppointmentUpdate, db: Session = Depends(database.get_db), current_user: models.Patient = Depends(oauth2.get_current_user)):
    appointment = apt_crud.get_appointment_by_id(appointment_id, db)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The appointment with id '%s' does not exist" % appointment_id
        )
    
    patient = pat_crud.get_patient_by_id(current_user.id, db)
    if appointment.patient_id != int(patient.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to perform this action."
        )
    
    appointment = apt_crud.update_appointment(appointment_id, payload, db)
    return {
        "message": "Appointment updated successfully",
        "detail": appointment}

@router.delete('/appointments/{appointment_id}', status_code=status.HTTP_202_ACCEPTED)
def delete_appointment(appointment_id: int, db: Session = Depends(database.get_db), current_user: models.Patient = Depends(oauth2.get_current_user)):
    appointment = apt_crud.get_appointment_by_id(appointment_id, db)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The appointment with id '%s' does not exist" % appointment_id
        )
    
    patient = pat_crud.get_patient_by_id(current_user.id, db)
    if appointment.patient_id != int(patient.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to perform this action."
        )
    
    apt_crud.cancel_appointment(appointment_id, db)
    return {"message": "Appointment deleted successfully"}