from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum
from typing import List

class AppointmentStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PatientBase(BaseModel):
    title: str = "Mr"
    first_name: str = "John"
    last_name: str = "Doe"
    email: EmailStr
    phone_number: str
    date_of_birth: datetime
    gender: str
    age: Optional[int] = None
    address_line1: str
    address_line2: Optional[str] = None
    city: str = "Ikeja"
    state: str = "Lagos"
    zip_code: str
    country: str = "Nigeria"
    hospital_card_id: str = "MEDFLOW/PAT/24/001"
    

class PatientCreate(PatientBase):
    hashed_password: str

class PatientUpdate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    is_active: bool = True

# Doctor schema definition
class DoctorBase(BaseModel):
    title: str = "Dr."
    first_name: str = "Henry"
    last_name: str = "Henry"
    email: EmailStr
    phone_number: str
    date_of_birth: datetime
    gender: str
    age: Optional[int] = None
    specialization: str = "Surgeon"
    address_line1: str
    address_line2: Optional[str] = None
    city: str = "Victoria Island"
    state: str = "Lagos"
    zip_code: str
    country: str = "Nigeria"
    hospital_id: str = "MEDFLOW/MED/SG/001"
    

class DoctorCreate(DoctorBase):
    hashed_password: str

class DoctorUpdate(DoctorBase):
    pass

class Doctor(DoctorBase):
    id: int
    is_available: bool = True


# Appointment schema definition
class AppointmentBase(BaseModel):
    id: int
    reason: str
    appointment_date: datetime

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    patient_id: int
    doctor_id: int
    emr_id: Optional[int] = None
    status: AppointmentStatus = AppointmentStatus.PENDING



# medical record schema definition
class EMR(BaseModel):
    id: int
    patient_id: int
    appointments: List[Appointment]