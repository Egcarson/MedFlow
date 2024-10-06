from fastapi import Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Optional
from app import models, schema

# create an appointment
# list appointments
# update an appointment
# cancel/delete an appointment

def create_appointment(payload: schema.AppointmentCreate, patient_id: int, db: Session) -> models.Appointment:
    appointment = models.Appointment(**payload.model_dump(), patient_id=patient_id)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

def get_appointment(offset: int, limit: int, db: Session) -> models.Appointment:
    return db.query(models.Appointment).offset(offset).limit(limit).all()

def get_appointments_by_patient_id(patient_id: int, db: Session) -> models.Appointment:
    return db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).all()

def status_validation(patient_id: int, appointment_id: int, db: Session) -> models.Appointment:
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id, models.Appointment.patient_id == patient_id).first()


def get_uncompleted_appointments(db: Session, patient_id: int):
    return db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id, or_(models.Appointment.status == schema.AppointmentStatus.PENDING, models.Appointment.status == schema.AppointmentStatus.IN_PROGRESS)).all()

def get_appointment_by_id(appointment_id: int, db: Session) -> models.Appointment:
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()

def update_appointment(appointment_id: int, payload: schema.AppointmentUpdate, db: Session) -> models.Appointment:
    appointment = get_appointment_by_id(appointment_id, db)
    if not appointment:
        return None
    
    apt_dict = payload.model_dump(exclude_unset=True)
    for k, v in apt_dict.items():
        setattr(appointment, k, v)
    
    db.commit()
    db.refresh(appointment)
    return appointment

def cancel_appointment(appointment_id: int, db: Session) -> models.Appointment:
    appointment = get_appointment_by_id(appointment_id, db)
    if not appointment:
        return None
    
    if appointment.status == schema.AppointmentStatus.PENDING:
        appointment.status = schema.AppointmentStatus.CANCELLED
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Appointment in-progress or completed cannot be cancelled')
    
    db.commit()
    db.refresh(appointment)
    
    return appointment

def check_pending_appointment(patient_id: int, db: Session):
    return db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id, models.Appointment.status == schema.AppointmentStatus.PENDING).first()

def switch_status(patient_id: int, appointment_id: int, payload: schema.AppointmentStatusSwitch, db: Session) -> models.Appointment:
    appointment = status_validation(patient_id, appointment_id, db)
    if not appointment:
        return None
    
    appointment.status = payload.status
    
    db.commit()
    db.refresh(appointment)
    
    return appointment