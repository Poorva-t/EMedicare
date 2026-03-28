# Medicare Healthcare Platform

A digital healthcare platform featuring smart doctor routing, AI-powered prescription suggestions, and video consultations.

## Features
- **Smart Doctor Matching:** Analyze symptoms to suggest the best specialist.
- **AI Prescriptions:** Automatically generate diagnoses and medicines based on symptoms.
- **Video Consultations:** Integrated Jitsi Meet for telehealth.
- **PDF Generation:** Download clean, formatted prescriptions.

## Setup Instructions

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Setup Environment Variables:**
Copy the `.env.example` file and rename it to `.env`:
```bash
cp .env.example .env
```
Inside `.env`, add your Groq API key:
`GROQ_API_KEY=your_actual_key_here`

3. **Initialize the Database:**
```bash
python seed_data.py
```
*(This creates the database and populates 10 realistic Indian doctors and a test patient).*

4. **Run the Application:**
You can double-click `setup_and_run.bat` or run:
```bash
python -m uvicorn main:app --port 8000
```

5. **Access the App:**
Open your browser to [http://localhost:8000](http://localhost:8000)

## Security Note
This project securely uses `python-dotenv` to manage secrets. **Never** commit your `.env` file!
