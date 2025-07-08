from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from utils.db import get_db
import qrcode
from bson import ObjectId

app = FastAPI()

class Patient(BaseModel):
    name: str
    dob: str
    blood_group: str
    allergies: List[str]
    chronic_diseases: List[str]
    medications: List[str]
    emergency_contacts: List[str]

def generate_qr(patient_id: str):
    # Generate QR code
    qr = qrcode.make(patient_id)
    # Save the QR code image
    qr.save(f"patient_{patient_id}_qr.png")
    print(f"QR code saved as 'patient_{patient_id}_qr.png'")

@app.post("/add-patient/")
def add_patient(patient: Patient):
    db = get_db()
    collection = db.patients
    patient_dict = patient.dict()
    result = collection.insert_one(patient_dict)
    
    # Generate QR code for the added patient
    patient_id = str(result.inserted_id)
    generate_qr(patient_id)
    
    return {"message": "Patient added successfully!", "id": patient_id}
