from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from utils.db import get_db
from bson import ObjectId
import cv2
import numpy as np
import qrcode
import os
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to generate QR code
def generate_qr(patient_id: str):
    qr = qrcode.make(patient_id)
    qr_code_path = f"qrcodes/patient_{patient_id}_qr.png"
    qr.save(qr_code_path)
    return qr_code_path

# API endpoint to trigger QR code generation for a single patient
@app.get("/generate-qr/{patient_id}")
async def generate_patient_qr(patient_id: str):
    try:
        qr_code_path = generate_qr(patient_id)
        return FileResponse(qr_code_path, media_type='image/png')
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# API endpoint to trigger QR code generation for all patients
@app.get("/generate-all-qr/")
async def generate_all_patient_qrs():
    db = get_db()
    collection = db.patients
    patient_ids = [str(patient["_id"]) for patient in collection.find()]
    
    qr_paths = []
    for patient_id in patient_ids:
        qr_path = generate_qr(patient_id)
        qr_paths.append(qr_path)
    
    return {"message": f"{len(qr_paths)} QR codes generated successfully!", "files": qr_paths}

class Patient(BaseModel):
    name: str
    dob: str
    blood_group: str
    allergies: List[str]
    chronic_diseases: List[str]
    medications: List[str]
    emergency_contacts: List[str]

@app.post("/add-patient/")
def add_patient(patient: Patient):
    db = get_db()
    collection = db.patients
    patient_dict = patient.dict()
    result = collection.insert_one(patient_dict)
    return {"message": "Patient added successfully!", "id": str(result.inserted_id)}

@app.get("/get-patient/{patient_id}")
def get_patient(patient_id: str):
    db = get_db()
    collection = db.patients
    try:
        patient = collection.find_one({"_id": ObjectId(patient_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid patient ID")

    if patient:
        patient["_id"] = str(patient["_id"])
        return patient
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

@app.put("/update-patient/{patient_id}")
def update_patient(patient_id: str, patient: Patient):
    db = get_db()
    collection = db.patients
    try:
        update_result = collection.update_one(
            {"_id": ObjectId(patient_id)},
            {"$set": patient.dict()}
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid patient ID")

    if update_result.matched_count:
        return {"message": "Patient updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

@app.delete("/delete-patient/{patient_id}")
def delete_patient(patient_id: str):
    db = get_db()
    collection = db.patients
    try:
        delete_result = collection.delete_one({"_id": ObjectId(patient_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid patient ID")

    if delete_result.deleted_count:
        return {"message": "Patient deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

@app.post("/scan-qr/")
async def scan_qr(file: UploadFile = File(...)):
    image_data = await file.read()
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    qr_detector = cv2.QRCodeDetector()
    data, bbox, _ = qr_detector.detectAndDecode(image)

    if not data:
        raise HTTPException(status_code=400, detail="No QR code detected")

    patient_id = data.strip()
    db = get_db()
    collection = db.patients
    try:
        patient = collection.find_one({"_id": ObjectId(patient_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid patient ID")

    if patient:
        patient["_id"] = str(patient["_id"])
        return patient
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/get-all-patients")
def get_all_patients():
    db = get_db()
    patients = list(db.patients.find())
    for patient in patients:
        patient["_id"] = str(patient["_id"])
    return patients
