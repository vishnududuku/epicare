const apiBase = 'http://localhost:8000';

document.getElementById('patientForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const formData = new FormData(e.target);
  const payload = {
    name: formData.get('name'),
    dob: formData.get('dob'),
    blood_group: formData.get('blood_group'),
    allergies: formData.get('allergies').split(','),
    chronic_diseases: formData.get('chronic_diseases').split(','),
    medications: formData.get('medications').split(','),
    emergency_contacts: formData.get('emergency_contacts').split(','),
  };

  const res = await fetch(`${apiBase}/add-patient/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  alert(`Patient added with ID: ${data.id}`);
  e.target.reset();
});

async function generateQr() {
  const patientId = document.getElementById('qrPatientId').value;
  const res = await fetch(`${apiBase}/generate-qr/${patientId}`);
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  document.getElementById('qrResult').innerHTML = `<img src="${url}" alt="QR Code">`;
}

async function scanQr() {
  const fileInput = document.getElementById('qrFile');
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${apiBase}/scan-qr/`, {
    method: 'POST',
    body: formData,
  });

  const data = await res.json();
  document.getElementById('scanResult').textContent = JSON.stringify(data, null, 2);
}