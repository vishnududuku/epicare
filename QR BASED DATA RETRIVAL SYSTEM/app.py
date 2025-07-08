from fastapi import FastAPI
from utils.db import get_db

app = FastAPI()

@app.get("/patients")
def get_patients():
    db = get_db()
    patients = list(db["patients"].find({}, {"_id": 0}))
    return patients