from app import models, schema
from sqlalchemy.orm import Session



class PatientCRUDServices:

    @staticmethod
    def create_patient(db: Session, payload: schema.PatientCreate, hashed_password: str):
        patient = models.Patient(
            **payload.model_dump(),
            hashed_password=hashed_password
        )

        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient
    
    @staticmethod
    def get_patients(db: Session, offset: int = 0, limit: int = 10):
        return db.query(models.Patient).offset(offset).limit(limit).all()
    
    @staticmethod
    def get_patient_by_email(db: Session, email: str):
        return db.query(models.Patient).filter(models.Patient.email == email).first()
    
    @staticmethod
    def get_patient_by_hospital_id(db: Session, hospital_id: str):
        return db.query(models.Patient).filter(models.Patient.hospital_card_id == hospital_id).first()
    
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