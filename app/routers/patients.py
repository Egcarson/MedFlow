from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.crud.patients import patient_crud_service as pat_crud
from app import schema, database, models, oauth2

router = APIRouter(
    tags=['Patients']
    )

#retrieve patients information
@router.get('/patients', status_code=status.HTTP_200_OK, response_model=List[schema.Patient])
def get_patients(offset: int = 0, limit: int = 10, search: Optional[str] = "", db: Session = Depends(database.get_db)):
    patients = pat_crud.get_patients(offset, limit, search, db)
    return patients

@router.get('/patients/{id}', status_code=status.HTTP_200_OK, response_model=schema.Patient)
def get_patient_by_id(id: int, db: Session = Depends(database.get_db)):
    patient = pat_crud.get_patient_by_id(id, db)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The patient with id '%s' does not exist" % id
        )
    return patient


@router.put('/patients/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schema.Patient)
def update_patient(id: int, payload: schema.PatientUpdate, db: Session = Depends(database.get_db), current_user: models.Patient = Depends(oauth2.get_current_user)):
    patient = pat_crud.get_patient_by_id(id, db)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The patient with id '%s' does not exist" % id
        )
    
    # intializing authourization logic
    user = pat_crud.get_patient_by_id(current_user.id, db)

    if patient.id != int(user.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to perform this action."
        )
    
    updated_patient = pat_crud.update_patient(db, id, payload)
    
    return updated_patient


@router.delete('/patients/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_patient(id: int, db: Session = Depends(database.get_db), current_user: models.Patient = Depends(oauth2.get_current_user)):
    patient = pat_crud.get_patient_by_id(id, db)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The patient with id '%s' does not exist" % id
            )
        
    # intializing authourization logic
    user = pat_crud.get_patient_by_id(current_user.id, db)
    if patient.id != int(user.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to perform this action."
        )
    
    pat_crud.delete_patient(id, db)

    return{"message": "Account deleted successfully!"}