import database
import models
import bcrypt

# Create tables
models.database.Base.metadata.create_all(bind=database.engine)

db = database.SessionLocal()

# Seed patient (if doesn't exist)
if not db.query(models.User).filter(models.User.email == "patient@health.com").first():
    hashed_password = bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    pt = models.User(name="Rahul Verma", email="patient@health.com", password_hash=hashed_password, role="patient")
    db.add(pt)

doctors_data = [
    {"name": "Dr. Rajesh Kumar", "email": "dr.rajesh@medicare.com", "spec": "Cardiologist", "exp": 15, "desc": "Expert in heart conditions and surgeries."},
    {"name": "Dr. Priya Sharma", "email": "dr.priya@medicare.com", "spec": "Neurologist", "exp": 12, "desc": "Specializes in brain and nervous system disorders."},
    {"name": "Dr. Amit Patel", "email": "dr.amit@medicare.com", "spec": "Orthopedic", "exp": 10, "desc": "Bone and joint specialist, focuses on sports injuries."},
    {"name": "Dr. Sneha Desai", "email": "dr.sneha@medicare.com", "spec": "Dermatologist", "exp": 8, "desc": "Treats skin conditions, rashes, and hair fall problems."},
    {"name": "Dr. Anjali Iyer", "email": "dr.anjali@medicare.com", "spec": "Gynecologist", "exp": 20, "desc": "Comprehensive women's health and maternity care."},
    {"name": "Dr. Vikram Singh", "email": "dr.vikram@medicare.com", "spec": "Urologist", "exp": 14, "desc": "Kidney stones and urinary tract health expert."},
    {"name": "Dr. Rohan Gupta", "email": "dr.rohan@medicare.com", "spec": "Pediatrician", "exp": 11, "desc": "Dedicated to child healthcare and vaccinations."},
    {"name": "Dr. Kavita Menon", "email": "dr.kavita@medicare.com", "spec": "ENT Specialist", "exp": 9, "desc": "Ear, Nose, and Throat specialist."},
    {"name": "Dr. Sameer Joshi", "email": "dr.sameer@medicare.com", "spec": "Psychiatrist", "exp": 18, "desc": "Mental health professional specializing in depression and anxiety."},
    {"name": "Dr. Neha Kapoor", "email": "dr.neha@medicare.com", "spec": "General Physician", "exp": 5, "desc": "First point of contact for fever, colds, and general wellness."}
]

for doc in doctors_data:
    if not db.query(models.User).filter(models.User.email == doc["email"]).first():
        hashed_password = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        d = models.User(name=doc["name"], email=doc["email"], password_hash=hashed_password, role="doctor", specialization=doc["spec"], experience=doc["exp"], description=doc["desc"])
        db.add(d)

db.commit()
print("Database seeded with patient (password: password) and 10 doctors (password: password123)")

