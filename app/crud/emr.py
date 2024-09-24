from app import models, schema
from app.crud.patients import patient_crud_service
from sqlalchemy.orm import Session


class EmrCRUDServices:

    @staticmethod
    def create_patient_EMR(db: Session, payload: schema.EMRCreate):
        patient = patient_crud_service.get_patient_by_hospital_id(db, hospital_id=payload.hospital_id)
        if not patient:
            return None
        
        appointments = 
        EMR = models.EMR(
            **payload.model_dump()
        )

        appointments = 

        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient


    @staticmethod
    def get_patient_EMR(db: Session, hospital_id: str):
        patient = patient_crud_service.get_patient_by_hospital_id(db, hospital_id=hospital_id)
        if not patient:
            return None
        return db.query(models.EMR).filter(patient.hospital_card_id == hospital_id).first()
        


    @staticmethod
    def delete_patient_EMR(db: Session, hospital_id: int):
        EMR = emr_crud_service.get_patient_EMR(db, hospital_id=hospital_id)

        db.delete(EMR)
        db.commit()

        return None


emr_crud_service = EmrCRUDServices()
