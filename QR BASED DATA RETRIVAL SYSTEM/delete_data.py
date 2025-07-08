from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from bson import ObjectId
from bson.errors import InvalidId
from utils.db import get_db
app = FastAPI()
# Reuse the same ObjectId validation helper
def validate_object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid patient ID format")

@app.delete("/delete-patient/{patient_id}")
def delete_patient(patient_id: str):
    db = get_db()
    collection = db.patients
    object_id = validate_object_id(patient_id)

    delete_result = collection.delete_one({"_id": object_id})
    if delete_result.deleted_count:
        return {"message": "Patient deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Patient not found")
