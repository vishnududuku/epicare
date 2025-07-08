import qrcode
from utils.db import get_db
from bson import ObjectId

# Function to generate QR code
def generate_qr(patient_id: str):
    qr = qrcode.make(patient_id)
    qr.save(f"qrcodes/patient_{patient_id}_qr.png")
    print(f"QR code saved as 'qrcodes/patient_{patient_id}_qr.png'")

# Function to fetch patient IDs from the database
def fetch_patient_ids():
    db = get_db()  # Get the database connection
    collection = db.patients  # Assuming 'patients' collection contains patient records
    patient_ids = [str(patient["_id"]) for patient in collection.find()]
    return patient_ids

# Main function to automate the QR code generation
def automate_qr_code_generation():
    patient_ids = fetch_patient_ids()  # Fetch all patient IDs
    for patient_id in patient_ids:
        generate_qr(patient_id)  # Generate a QR code for each patient ID

if __name__ == "__main__":
    automate_qr_code_generation()  # Call the function to start the process
