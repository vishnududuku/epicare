import sqlite3

def create_table():
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            blood_group TEXT,
            height REAL,
            weight REAL,
            allergies TEXT,
            chronic_diseases TEXT,
            medications TEXT,
            emergency_contacts TEXT,
            last_known_vitals TEXT,
            insurance_details TEXT,
            recent_surgeries TEXT,
            image_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_patient(id, name, age, blood_group, height, weight, allergies,
                chronic_diseases, medications, emergency_contacts,
                last_known_vitals, insurance_details, recent_surgeries, image_url):
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO patients (
            id, name, age, blood_group, height, weight, allergies,
            chronic_diseases, medications, emergency_contacts,
            last_known_vitals, insurance_details, recent_surgeries, image_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        id, name, age, blood_group, height, weight, allergies,
        chronic_diseases, medications, emergency_contacts,
        last_known_vitals, insurance_details, recent_surgeries, image_url
    ))
    conn.commit()
    conn.close()

def get_all_patients():
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute('SELECT * FROM patients')
    patients = c.fetchall()
    conn.close()
    return patients