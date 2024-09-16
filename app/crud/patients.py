from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional
from app import models, schema



class PatientCRUDServices:

    @staticmethod
    def create_patient(db: Session, payload: schema.PatientCreate):

        patient = models.Patient(**payload.model_dump())

        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient
    
    @staticmethod
    def get_patients(offset: int = 0, limit: int = 10, search: Optional[str] = "", db: Session = Depends()) -> models.Patient:
        return db.query(models.Patient).filter((models.Patient.hospital_card_id.contains(search.upper())) | (models.Patient.last_name.contains(search.title()))).offset(offset).limit(limit).all() # the filtering will enable the admin retrieve patients by a specific year or pattern using the card_id (e.g MEDFLOW/PAT/24/001 -> MEDFLOW/PAT/24 will retrieve only a specific year 2024 or MEDFLOW/PAT/23 etc...) or by last name
    
    @staticmethod
    def get_patient_by_email(db: Session, email: str):
        return db.query(models.Patient).filter(models.Patient.email == email).first()

    @staticmethod
    def get_patient_by_id(id: int, db: Session):
        return db.query(models.Patient).filter(models.Patient.id == id).first()
    
    @staticmethod
    def get_patient_by_hospital_id(db: Session, hospital_id: str) -> models.Patient:
        return db.query(models.Patient).filter(models.Patient.hospital_card_id == hospital_id).first()
    
    @staticmethod
    def update_patient(db: Session, id: int, payload: schema.PatientUpdate):
        patient = db.query(models.Patient).filter(models.Patient.id == id).first()
        if not patient:
            return None
        
        patient_dict = payload.model_dump(exclude_unset=True)
        for k, v in patient_dict.items():
            setattr(patient, k, v)

        db.commit()
        db.refresh(patient)
        return patient
    
    @staticmethod
    def delete_patient(id: int, db: Session):
        patient = PatientCRUDServices.get_patient_by_id(id, db)
        if not patient:
            return None

        db.delete(patient)
        db.commit()
        return patient



    # To check if patient Email or ID in database
    @staticmethod
    def get_patient(db: Session, credential: str):
        patient = patient_crud_service.get_patient_by_email(db, email=credential)
        if not patient:
            patient = patient_crud_service.get_patient_by_hospital_id(db, hospital_id=credential)
        if not patient:
            return None
        return patient








patient_crud_service = PatientCRUDServices()