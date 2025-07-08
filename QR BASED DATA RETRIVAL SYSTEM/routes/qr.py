# routes/qr.py
import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.db import get_db
from bson import ObjectId

router = APIRouter()

@router.post("/scan-qr/")
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
    patient = db.patients.find_one({"_id": ObjectId(patient_id)})

    if patient:
        patient["_id"] = str(patient["_id"])
        return patient
    else:
        raise HTTPException(status_code=404, detail="Patient not found")
