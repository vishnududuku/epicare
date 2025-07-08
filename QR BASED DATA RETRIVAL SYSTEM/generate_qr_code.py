import qrcode

def generate_qr(patient_id: str):
    qr = qrcode.make(patient_id)
    qr.save(f"qrcodes/patient_{patient_id}_qr.png")
    print(f"QR code saved as 'qrcodes/patient_{patient_id}_qr.png'")

if __name__ == "__main__":
    patient_id = "67fa5118450bfb849e44231c"  # Replace with an actual patient ID
    generate_qr(patient_id)
