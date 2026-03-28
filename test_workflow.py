import requests
import time
import os

BASE_URL = "http://localhost:8002"

print("--- Starting Verification ---")

# Wait for server to be up
time.sleep(2)

# 1. Login patient
resp = requests.post(f"{BASE_URL}/api/login", json={"email": "patient@health.com", "password": "password"})
assert resp.status_code == 200, f"Patient login failed: {resp.text}"
patient_token = resp.json()["access_token"]
headers_pt = {"Authorization": f"Bearer {patient_token}"}

# 2. Login doctor
resp = requests.post(f"{BASE_URL}/api/login", json={"email": "doctor@health.com", "password": "password"})
assert resp.status_code == 200, f"Doctor login failed: {resp.text}"
doc_token = resp.json()["access_token"]
doc_id = resp.json()["id"]
headers_doc = {"Authorization": f"Bearer {doc_token}"}

# 3. Create appointments (Routine, Fever, Chest pain)
print("Creating appointments...")
requests.post(f"{BASE_URL}/api/appointments", headers=headers_pt, json={"doctor_id": doc_id, "date_time": "2024-01-01T10:00", "symptoms": "Just a routine checkup"})
requests.post(f"{BASE_URL}/api/appointments", headers=headers_pt, json={"doctor_id": doc_id, "date_time": "2024-01-01T11:00", "symptoms": "High fever and pain"})
requests.post(f"{BASE_URL}/api/appointments", headers=headers_pt, json={"doctor_id": doc_id, "date_time": "2024-01-01T12:00", "symptoms": "Severe chest pain and breathing issues"})

# 4. Fetch as doctor and check priority ordering
resp = requests.get(f"{BASE_URL}/api/appointments", headers=headers_doc)
appts = resp.json()
print("Doctor appointments order:")
for a in appts:
    print(f"- {a['symptoms']}")

# Priority expects: Chest pain (10) -> Fever (5) -> Routine (2)
assert "chest pain" in appts[0]['symptoms'].lower(), "Priority 10 failed!"
assert "fever" in appts[1]['symptoms'].lower(), "Priority 5 failed!"
assert "routine" in appts[2]['symptoms'].lower(), "Priority 2 failed!"
print("Priority sorting passed!")

appt_id = appts[0]['id']

# 5. Test AI Prescription
print("Testing AI Engine...")
resp = requests.post(f"{BASE_URL}/api/ai/generate-prescription", headers=headers_doc, json={"symptoms": "Severe chest pain", "history": "None"})
ai_res = resp.json()
print("AI Response:", ai_res)
assert "diagnosis" in ai_res

# 6. Save Prescription and check PDF
print("Saving prescription (PDF generation)...")
resp = requests.post(f"{BASE_URL}/api/appointments/{appt_id}/prescription", headers=headers_doc, json={
    "symptoms": "Severe chest pain",
    "diagnosis": ai_res["diagnosis"],
    "medicines": ai_res["medicines"],
    "advice": ai_res["advice"],
    "follow_up": "Immediate"
})
assert resp.status_code == 200, f"Prescription save failed: {resp.text}"

pdf_path = f"prescriptions/prescription_{appt_id}.pdf"
assert os.path.exists(pdf_path), f"PDF file not found at {pdf_path}!"
print("PDF Generation passed!")

print("--- Verification Complete ---")
