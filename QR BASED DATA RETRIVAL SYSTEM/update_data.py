from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from bson import ObjectId
from utils.db import get_db

# ✅ Define app before using it
app = FastAPI()

# ✅ Define Patient model (if not already defined)
class Patient(BaseModel):
    name: str
    dob: str
    blood_group: str
    allergies: List[str]
    chronic_diseases: List[str]
    medications: List[str]
    emergency_contacts: List[str]

# ✅ Update patient endpoint
@app.put("/update-patient/{patient_id}")
def update_patient(patient_id: str, patient: Patient):
    db = get_db()
    collection = db.patients
    update_result = collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": patient.dict()}
    )
    if update_result.matched_count:
        return {"message": "Patient updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Patient not found")
