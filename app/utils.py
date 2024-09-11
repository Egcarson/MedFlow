from passlib.context import CryptContext

# Define the password hashing context

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

# verify hashed password for user authentication
def verify_hashed_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)