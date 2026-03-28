from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import AIPredictRequest, AIPredictResponse

app = FastAPI(title="AI Diagnostic Microservice")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lightweight keyword matching dict
SYMPTOM_DB = {
    "fever": {
        "diagnosis": "Viral Fever",
        "medicines": "Paracetamol 500mg (1-0-1)",
        "advice": "Rest, drink plenty of fluids"
    },
    "cough": {
        "diagnosis": "Common Cold / Seasonal Cough",
        "medicines": "Cough Syrup (2 tsp SOS)",
        "advice": "Avoid cold foods, do warm water gargles"
    },
    "headache": {
        "diagnosis": "Tension Headache / Migraine",
        "medicines": "Ibuprofen 400mg (SOS)",
        "advice": "Reduce screen time, sleep 8 hours"
    },
    "stomach ache": {
        "diagnosis": "Gastritis / Indigestion",
        "medicines": "Antacid Gel (2 tsp before meals)",
        "advice": "Eat bland food, avoid spicy/oily food"
    }
}

@app.post("/predict", response_model=AIPredictResponse)
def predict(request: AIPredictRequest):
    symptoms = request.symptoms.lower()
    
    predicted_diagnosis = []
    predicted_medicines = []
    predicted_advice = []

    for keyword, info in SYMPTOM_DB.items():
        if keyword in symptoms:
            predicted_diagnosis.append(info["diagnosis"])
            predicted_medicines.append(info["medicines"])
            predicted_advice.append(info["advice"])

    if not predicted_diagnosis:
        return AIPredictResponse(
            diagnosis="General Malaise / Needs Observation",
            medicines="Supportive Care as needed",
            advice="Please consult the doctor for a detailed physical checkup."
        )
    
    return AIPredictResponse(
        diagnosis=", ".join(predicted_diagnosis),
        medicines="\n".join(predicted_medicines),
        advice="\n".join(predicted_advice)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
