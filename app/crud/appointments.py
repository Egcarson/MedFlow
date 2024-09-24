from app import models, schema
from app.crud.patients import patient_crud_service
from sqlalchemy.orm import Session


class AppointmentCRUDServices:


    @staticmethod
    def get_appointment_by_hospital_id(db: Session, hospital_id: int, patient_id):
        patient = patient_crud_service.get_patient_by_hospital_id(db, hospital_id)
        if not patient:
            return None
        return db.query(models.Appointment).filter(patient_id)
