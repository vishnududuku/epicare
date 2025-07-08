import cv2

def read_qr(image_path: str):
    # Read the image containing the QR code
    img = cv2.imread(image_path)

    # Create a QRCodeDetector object
    detector = cv2.QRCodeDetector()

    # Detect and decode the QR code
    retval, decoded_info, points, straight_qrcode = detector(img)

    if retval:
        # Print the decoded information (patient ID in this case)
        print(f"Decoded QR code data: {decoded_info}")
    else:
        print("QR code not detected")

if __name__ == "__main__":
    # Path to the QR code image you want to read
    image_path = "qrcodes/patient_12345_qr.png"  # Replace with the path of your generated QR code
    read_qr(image_path)
