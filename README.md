# EPICARE

EPICARE is an AI-powered system designed for rapid emergency patient identification and intelligent care management. It integrates facial recognition, QR code scanning, and secure cloud-based electronic health records (EHRs) to provide a seamless healthcare experience in critical scenarios.

## 🔍 Project Objective

To improve emergency response and patient safety by enabling quick access to medical history through multimodal biometric identification and AI-driven support tools.

## 🚀 Features

- 🔐 *Secure User Authentication* using facial recognition and QR codes.
- 🧠 *AI-powered Health Chatbot* for immediate medical queries.
- 💊 *Prescription Upload & Reminder System* for timely medication alerts.
- 📊 *Drug Interaction Prediction* using patient-specific medication data.
- 🍎 *Health Recommendations* including diet and fitness plans.
- 📷 *Face Encoding using LBPH* for accurate biometric matching.
- 📦 *Data Storage with MongoDB* ensuring scalable and secure record-keeping.
- 🧾 *QR Code Generation* for fast offline/online patient data retrieval.

## 🛠 Tech Stack

- *Frontend*: Streamlit
- *Backend*: FastAPI
- *Database*: MongoDB
- *Libraries*: OpenCV, face-recognition, QRCode, NumPy, scikit-learn, PyMongo

## 🧪 Model Performance
| Metric     | Value  | Remarks                                     |
|------------|--------|---------------------------------------------|
| Accuracy   | 95.6%  | Tested on mixed dataset (LFW + manual faces)|
| Precision  | 0.93   | High confidence in face matches             |
| Recall     | 0.91   | Works well even in poor lighting conditions |

---
