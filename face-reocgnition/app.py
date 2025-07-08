import streamlit as st
import cv2
import numpy as np
import uuid
import pickle
import os
from db import create_table, add_patient, get_all_patients
from utils import upload_image

# ---------- CONFIG ----------
MODEL_PATH = "face_model.yml"
LABEL_MAP_PATH = "label_map.pkl"

# ---------- SETUP ----------
create_table()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer.create()

# Load model if exists
if os.path.exists(MODEL_PATH):
    recognizer.read(MODEL_PATH)
    label_map = pickle.load(open(LABEL_MAP_PATH, "rb"))
else:
    label_map = {}

# ---------- UI ----------
st.title("Patient Face Recognition System")
tab1, tab2, tab3 = st.tabs(["Display Patients", "Upload Patient", "Scan Patient"])

# ---------- DISPLAY PATIENTS ----------
with tab1:
    st.subheader("All Patients Data")
    patients = get_all_patients()
    for patient in patients:
        st.write(f"ID: {patient[0]}\nName: {patient[1]}\nAge: {patient[2]}\nMedications: {patient[3]}")
        st.image(patient[13])

# ---------- UPLOAD PATIENT ----------
with tab2:
    import uuid
    st.subheader("Add New Patient Data")
    with st.form(key='patient_form'):
        image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        height = st.number_input("Height (cm)", min_value=30.0, max_value=250.0)
        weight = st.number_input("Weight (kg)", min_value=2.0, max_value=300.0)
        allergies = st.text_area("Allergies")
        chronic_diseases = st.text_area("Chronic Diseases")
        medications = st.text_area("Medications")
        emergency_contacts = st.text_area("Emergency Contacts (Name, Relation, Phone)")
        last_known_vitals = st.text_area("Last Known Vitals (BP, HR, etc.)")
        insurance_details = st.text_area("Insurance Details")
        recent_surgeries = st.text_area("Recent Surgeries")
        
        submit_button = st.form_submit_button(label='Submit')

        if submit_button and image_file:
            patient_id = str(uuid.uuid4())
            image_url = upload_image(image_file, patient_id)
            st.image(image_file, caption="Captured Image")

            # Add patient to database
            add_patient(
                patient_id, name, age, blood_group, height, weight, allergies,
                chronic_diseases, medications, emergency_contacts,
                last_known_vitals, insurance_details, recent_surgeries, image_url
            )

            # Train the model
            image_file.seek(0)
            img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                label = len(label_map)
                label_map[label] = patient_id

                if os.path.exists(MODEL_PATH):
                    recognizer.update([face], np.array([label]))
                else:
                    recognizer.train([face], np.array([label]))

                recognizer.save(MODEL_PATH)
                with open(LABEL_MAP_PATH, "wb") as f:
                    pickle.dump(label_map, f)

            st.success("Patient added and face model updated.")

# ---------- SCAN PATIENT ----------
# with tab3:
#     st.subheader("Scan a Patient")
#     image_file = st.file_uploader("Upload Image for Recognition", type=["jpg", "jpeg", "png"])
#     if image_file:
#         img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#         for (x, y, w, h) in faces:
#             face = gray[y:y+h, x:x+w]
#             label, confidence = recognizer.predict(face)
#             patient_id = label_map.get(label, None)

#             if patient_id:
#                 flag = False
#                 st.write(f"Recognized Patient ID: {patient_id}")
#                 patients = get_all_patients()
#                 for patient in patients:
#                     if patient[0] == patient_id:
#                         st.write(f"Name: {patient[1]}")
#                         st.write(f"Age: {patient[2]}")
#                         st.write(f"Medications: {patient[3]}")
#                         st.image(patient[4])
#                         flag = True
#                         break
#                 if flag:
#                     break
#             else:
#                 st.error("Patient not found.")

# with tab3:
#     st.subheader("Scan a Patient")

#     camera_image = st.camera_input("Take a picture")

#     if camera_image:
#         img = cv2.imdecode(np.frombuffer(camera_image.read(), np.uint8), cv2.IMREAD_COLOR)
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#         for (x, y, w, h) in faces:
#             face = gray[y:y+h, x:x+w]
#             label, confidence = recognizer.predict(face)
#             patient_id = label_map.get(label, None)

#             if patient_id:
#                 flag = False
#                 st.success(f"✅ Recognized Patient ID: {patient_id}")
#                 patients = get_all_patients()
#                 for patient in patients:
#                     if patient[0] == patient_id:
#                         st.write(f"Name: {patient[1]}")
#                         st.write(f"Age: {patient[2]}")
#                         st.write(f"Medications: {patient[3]}")
#                         st.image(patient[4])
#                         flag = True
#                         break
#                 if flag:
#                     break
#             else:
#                 st.error("❌ Patient not found.")


# with tab3:
#     st.subheader("Scan a Patient")

#     camera_image = st.camera_input("Take a picture")

#     if camera_image:
#         img = cv2.imdecode(np.frombuffer(camera_image.read(), np.uint8), cv2.IMREAD_COLOR)
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#         # Draw rectangles and mock landmarks
#         for (x, y, w, h) in faces:
#             cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#             # Mock landmarks (center of eyes & mouth approx)
#             cv2.circle(img, (x + int(w*0.3), y + int(h*0.35)), 5, (255, 0, 0), -1)  # Left eye
#             cv2.circle(img, (x + int(w*0.7), y + int(h*0.35)), 5, (255, 0, 0), -1)  # Right eye
#             cv2.circle(img, (x + int(w*0.5), y + int(h*0.7)), 5, (0, 0, 255), -1)  # Mouth

#             face = gray[y:y+h, x:x+w]
#             label, confidence = recognizer.predict(face)
#             patient_id = label_map.get(label, None)

#             st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Detected Face with Fun Landmarks")

#             if patient_id:
#                 st.success(f"✅ Recognized Patient ID: {patient_id}")
#                 patients = get_all_patients()
#                 for patient in patients:
#                     if patient[0] == patient_id:
#                         st.write(f"Name: {patient[1]}")
#                         st.write(f"Age: {patient[2]}")
#                         st.write(f"Medications: {patient[3]}")
#                         st.image(patient[4])
#                         break
#             else:
#                 st.error("❌ Patient not found.")





with tab3:
    st.subheader("Scan a Patient")

    camera_image = st.camera_input("Take a picture")

    if camera_image:
        img = cv2.imdecode(np.frombuffer(camera_image.read(), np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Structured "landmarks" (mimicking mesh manually)
            points = [
                (x + int(w*0.1), y + int(h*0.8)),  # jaw left
                (x + int(w*0.3), y + int(h*0.9)),  # jaw mid-left
                (x + int(w*0.5), y + int(h*0.95)), # chin center
                (x + int(w*0.7), y + int(h*0.9)),  # jaw mid-right
                (x + int(w*0.7), y + int(h*0.8)),  # jaw right

                (x + int(w*0.3), y + int(h*0.4)),  # left eye
                (x + int(w*0.7), y + int(h*0.4)),  # right eye
                (x + int(w*0.5), y + int(h*0.6)),  # nose tip
                (x + int(w*0.4), y + int(h*0.7)),  # mouth left
                (x + int(w*0.6), y + int(h*0.7)),  # mouth right

                (x + int(w*0.2), y + int(h*0.2)),  # forehead left
                (x + int(w*0.8), y + int(h*0.2))   # forehead right
            ]

            # Draw dots
            for pt in points:
                cv2.circle(img, pt, 4, (255, 0, 0), -1)  # Blue

            # Draw links (basic mesh)
            links = [
                (0, 1), (1, 2), (2, 1), (3, 2),      # jawline
                (5, 6), (5, 7), (6, 7),              # eyes to nose
                (7, 8), (7, 9),                      # nose to mouth
                (8, 9),                              # mouth width
                (10, 11), (10, 5), (11, 6),          # forehead to eyes
                (10, 0), (11, 4)                     # forehead to jaw
            ]
            for i, j in links:
                cv2.line(img, points[i], points[j], (200, 255, 255), 1)  # Light blue

            face = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(face)
            
            patient_id = label_map.get(label, None)

            st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Facial Mesh Approximation")

            if patient_id:
                st.success(f"✅ Recognized Patient ID: {patient_id}")
                patients = get_all_patients()
                
                flag = False
                for patient in patients:
                    if patient[0] == patient_id:
                        st.write(f"Name: {patient[1]}")
                        st.write(f"Age: {patient[2]}")
                        st.write(f"Blood Group: {patient[3]}")
                        st.write(f"Height: {patient[4]}")
                        st.write(f"Weight: {patient[5]}")
                        st.write(f"Allergies: {patient[6]}")
                        st.write(f"Chronic Diseases: {patient[7]}")
                        st.write(f"Medications: {patient[8]}")
                        st.image(patient[13])
                        flag = True
                        break
                if flag:
                    break
            else:
                st.error("❌ Patient not found.")
