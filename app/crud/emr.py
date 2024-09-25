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
    def get_patient_EMR(db: Session, patient_id: str):
        patient = patient_crud_service.get_patient_by_id(db, patient_id)
        if not patient:
            return None
        return db.query(models.EMR).filter(patient_id == patient_id).first()
        


    @staticmethod
    def delete_patient_EMR(db: Session, patient_id: int):
        Emr = emr_crud_service.get_patient_EMR(db, patient_id)

        db.delete(Emr)
        db.commit()

        return None


emr_crud_service = EmrCRUDServices()
