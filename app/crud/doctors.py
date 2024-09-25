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
    
    @staticmethod
    def get_all_doctors(db: Session, offset: int = 0, limit: int = 10):
        return db.query(models.Doctor).offset(offset).limit(limit).all()
    
    @staticmethod
    def get_doctor_by_id(db: Session, doctor_id: int):
        return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    
    @staticmethod
    def get_doctor_by_specialization(db: Session, specialization: str, offset: int = 0, limit: int = 10):
        return db.query(models.Doctor).filter(models.Doctor.specialization == specialization).offset(offset).limit(limit).all()
    
    @staticmethod
    def change_doctor_availability_status(db: Session, doctor_id: int):
        doctor = doctor_crud_service.get_doctor_by_id(db, doctor_id=doctor_id)
        if not doctor:
            return None
        if doctor.is_available:
            doctor.is_available = False
        else:
            doctor.is_available = True
        
        return doctor
    
    @staticmethod
    def update_doctor(db: Session, payload: schema.DoctorUpdate, doctor_id: int):
        doctor = doctor_crud_service.get_doctor_by_id(db, doctor_id=doctor_id)
        if not doctor:
            return None
        
        payload_dict = payload.model_dump(exclude_unset=True)

        for key, value in payload_dict.items():
            setattr(doctor, key, value)

        db.add(doctor)
        db.commit()
        db.refresh(doctor)

        return doctor
    
    @staticmethod
    def delete_doctor(db: Session, doctor_id: int):
        doctor = doctor_crud_service.get_doctor_by_id(db, doctor_id=doctor_id)
        
        db.delete(doctor)
        db.commit()

        return None
        
        


doctor_crud_service = DoctorCRUDServices()
