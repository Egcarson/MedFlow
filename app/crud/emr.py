from app import models, schema
from app.crud.appointment import get_appointments_by_patient_id
from app.crud.patients import patient_crud_service
from sqlalchemy.orm import Session


class EmrCRUDServices:

    @staticmethod
    def create_patient_EMR(db: Session, payload: schema.EMRCreate, patient_id: int):
        patient = patient_crud_service.get_patient_by_id(patient_id, db)
        if not patient:
            return None
        
        appointments = get_appointments_by_patient_id(patient_id, db)
        Emr = models.EMR(
            **payload.model_dump(),
            appointments=appointments
        )

        db.add(Emr)
        db.commit()
        db.refresh(Emr)
        return Emr


    @staticmethod
    def get_patient_EMR(patient_id: int, db: Session):
        return db.query(models.EMR).filter(models.EMR.patient_id == patient_id).all()
    
    @staticmethod
    def get_patient_EMR2(patient_id: int, emr_id: int, db: Session):
        return db.query(models.EMR).filter(models.EMR.id == emr_id, models.EMR.patient_id == patient_id).first() # single validation


    @staticmethod
    def delete_patient_EMR(patient_id: int, emr_id: int, db: Session):
        emr = emr_crud_service.get_patient_EMR2(patient_id, emr_id, db)

        if not emr:
            return None

        db.delete(emr)
        db.commit()
        
        return emr
    
    @staticmethod
    def validate_patient_doctor(patient_id: int, doctor_id: int, db: Session):
        return db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id, models.Appointment.doctor_id == doctor_id).all()


emr_crud_service = EmrCRUDServices()
