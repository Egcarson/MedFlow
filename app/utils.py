from sqlalchemy.orm import Session
from crud.doctors import doctor_crud_service
from crud.patients import patient_crud_service


# from passlib.context import CryptContext

# # Define the password hashing context

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str):
#     return pwd_context.hash(password)

# # verify hashed password for user authentication
# def verify_hashed_password(password, hashed_password):
#     return pwd_context.verify(password, hashed_password)


# For authentication to know whether the user exists as a patient or doctor in database
def get_user(db: Session, credential: str):
    user = patient_crud_service.get_patient(db, credential)
    if not user:
        user = doctor_crud_service.get_doctor(db, credential)
    return user
    