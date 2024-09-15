from app import models, schema
from sqlalchemy.orm import Session






class DoctorCRUDServices:

    @staticmethod
    def create_doctor(db: Session, payload: schema.DoctorCreate):
        doctor = models.Doctor(**payload.model_dump())

        db.add(doctor)
        db.commit()
        db.refresh(doctor)
        return doctor


    @staticmethod
    def get_doctor_by_email(db: Session, email: str):
        return db.query(models.Doctor).filter(models.Doctor.email == email).first()

    @staticmethod
    def get_doctor_by_hospital_id(db: Session, hospital_id: str):
        return db.query(models.Doctor).filter(models.Doctor.hospital_id == hospital_id).first()

    #  Check if doctor Email or Id is in database
    @staticmethod
    def get_doctor(db: Session, credential: str):
        doctor = doctor_crud_service.get_doctor_by_email(
            db, email=credential)
        if not doctor:
            doctor = doctor_crud_service.get_doctor_by_hospital_id(
                db, hospital_id=credential)
        if not doctor:
            return None
        return doctor


doctor_crud_service = DoctorCRUDServices()
