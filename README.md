# MedFlow API

MedFlow is a healthcare management API that streamlines the process of managing patient information, appointments, and electronic medical records (EMR). This project was developed as a collaboration between **Godprevail Eseh** and **Ojeh Henry**, with the aim of providing a robust and scalable solution for healthcare providers.

## Features

- **User Management**: Handles the creation of patient, doctors and various types of authentication.
- **Appointment Scheduling**: Enables patients to book appointments with doctors and view appointment history.
- **Electronic Medical Records (EMR)**: Automatically creates EMR for patients following a successful appointment, allowing doctors to update and view patient records.
- **Appointment History**: Tracks and logs past appointments and their related details for easy access.
- **EMR Deletion**: Provides functionality to delete a patient's EMR when necessary.

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: PostgreSQL (SQLAlchemy for ORM)
- **Authentication**: JWT-based authentication for secure access
- **ORM Tooling**: SQLAlchemy for database modeling and Alembic for migrations
- **Testing**: Pytest for automatic testing
- **Containerization**: Docker for deployment in a containerized environment

## Getting Started

### Prerequisites

- Python 3.12.x
- PostgreSQL
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Egcarson/MedFlow-API.git
   cd medflow-api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables:
   - Create a `.env` file and define the following variables:
     ```plaintext
     DATABASE_URL=postgresql://user:password@localhost/medflow_db
     SECRET_KEY=your_secret_key
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```

4. Apply database migrations:
   ```bash
   alembic upgrade head
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

### Running Tests

To run the automated tests using `pytest`:
```bash
pytest
```

## API Endpoints

### User Authentication

- **Signup**: `/signup/patient` (POST)  
  Allows new patients to sign up.

- **Signup**: `/signup/doctor` (POST)  
  Allows new doctors to sign up.

- **Login**: `/auth/login` (POST)  
  Authenticates users and provides a JWT token.

- **Password Reset**: `/auth/password_reset` (POST)  
  Allows new users to reset their passwords.

- **Appointment Status Switch**: `/admin/appointment_status` (PUT)  
  Allows admins/doctors to switch appointment status.

### Patients

- **Get Patients**: `/patient` (GET)  
  Get all patients available in the database.

- **Get Patients by ID**: `/patient/{id}` (GET)  
  Get patient by id if available in the database.

- **Update Patient**: `/patient/{id}` (PUT)  
  Update patient information by id if available in the database. (authentication needed)

- **Delete Patient**: `/patient/{id}` (DELETE)  
  Delete patient information by id if available in the database. (authentication needed)

### Doctors

- **Get Doctors**: `/doctors` (GET)  
  Get all doctors available in the database.

- **Get Doctor by Specialization**: `/doctors/specialization` (GET)  
  Get doctor by specializations if available in the database.

- **Get Doctor by ID**: `/doctors/{doctor_id}` (GET)  
  Get doctor by id if available in the database.

- **Update Doctor**: `/doctors/{doctor_id}` (PUT)  
  Update doctor information by id if available in the database. (authentication needed)

- **Delete Doctor**: `/doctors/{doctor_id}` (DELETE)  
  Delete doctor information by id if available in the database. (authentication needed)

- **Change Doctor Availability Status**: `/doctors/{doctor_id}/change_availability` (POST)  
  Change doctor's Availability status. (authentication needed)


### Appointments

- **Create Appointment**: `/appointments` (POST)  
  Creates appointment for patient. (authentication needed)

- **View Appointments**: `/appointments` (GET)  
  Retrieves a list of all appointments from the database.

- **View Appointment**: `/appointments/{patient_id}` (GET)  
  Retrieves a list of appointments for the logged-in user. (authentication required)

- **Update Appointment**: `/appointments/{appointment_id}` (PUT)  
  Update appointment for patient. (authentication required)

- **Delete Appointment**: `/appointments/{appointment_id}` (DELETE)  
  Delete appointment for patient. (authentication required)


### Electronic Medical Records (EMR)

- **View EMR**: `/emr/{patient_id}` (GET)  
  Allows doctors to view a patient’s medical record.

- **Update EMR**: `/emr/{patient_id}` (PUT)  
  Allows doctors to update the EMR of a patient.

- **Delete EMR**: `/emr/{emr_id}` (DELETE)  
  Allows deletion of a patient’s EMR.

## Deployment

The API can be deployed using Uvicorn. To ru the app, execute the following commands:

1. Start the app:
   ```bash
   uvicorn app.main:app --reload
   ```
The API can also be deployed using Docker. To build and run the Docker container, execute the following commands:

1. Build the Docker image:
   ```bash
   docker-compose 
   ```

2. Run the Docker container:
   ```bash
   docker-compuse
   ```