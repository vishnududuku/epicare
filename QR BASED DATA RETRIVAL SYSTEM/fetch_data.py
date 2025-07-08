from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from bson.errors import InvalidId
from utils.db import get_db

app = FastAPI()

# --- Patient Schema ---
class Patient(BaseModel):
    name: str
    dob: str
    blood_group: str
    allergies: List[str]
    chronic_diseases: List[str]
    medications: List[str]
    emergency_contacts: List[str]

class PatientOut(Patient):
    id: str  # Used instead of MongoDB's "_id"

# --- Helper Function ---
def validate_object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid patient ID format")

# --- Get Patient Endpoint ---
@app.get("/get-patient/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: str):
    db = get_db()
    collection = db.patients
    object_id = validate_object_id(patient_id)
    patient = collection.find_one({"_id": object_id})
    if patient:
        patient["id"] = str(patient["_id"])  # add new "id" field
        del patient["_id"]  # remove original ObjectId field
        return patient
    else:
        raise HTTPException(status_code=404, detail="Patient not found")
