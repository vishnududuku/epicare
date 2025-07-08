from pydantic import BaseModel
from typing import List

class Patient(BaseModel):
    name: str
    dob: str
    blood_group: str
    allergies: List[str]
    chronic_diseases: List[str]
    medications: List[str]
    emergency_contacts: List[str]
