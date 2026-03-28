from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
import database

class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="patient") # 'doctor' or 'patient'
    specialization = Column(String, nullable=True)
    experience = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)

    appointments_as_patient = relationship("Appointment", foreign_keys="[Appointment.patient_id]", back_populates="patient")
    appointments_as_doctor = relationship("Appointment", foreign_keys="[Appointment.doctor_id]", back_populates="doctor")

class Appointment(database.Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("users.id"))
    date_time = Column(String) # ISO format string for simplicity
    status = Column(String, default="pending") # pending, approved, completed, cancelled
    meeting_link = Column(String, nullable=True)
    symptoms = Column(Text, nullable=True)

    patient = relationship("User", foreign_keys=[patient_id], back_populates="appointments_as_patient")
    doctor = relationship("User", foreign_keys=[doctor_id], back_populates="appointments_as_doctor")
    prescription = relationship("Prescription", back_populates="appointment", uselist=False)

class Prescription(database.Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True)
    symptoms = Column(Text)
    diagnosis = Column(Text)
    medicines = Column(Text)
    advice = Column(Text)
    follow_up = Column(String, nullable=True)
    file_path = Column(String, nullable=True) # PDF path

    appointment = relationship("Appointment", back_populates="prescription")
