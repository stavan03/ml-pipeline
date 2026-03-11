from fastapi import FastAPI
import joblib
import numpy as np

# Load the saved model
model = joblib.load("models/model.pkl")

# Create the API
app = FastAPI()

@app.get("/")
def home():
    return {"message": "ML Model API is running!"}

@app.post("/predict")
def predict(features: list[float]):
    # Convert input to numpy array and reshape for the model
    data = np.array(features).reshape(1, -1)
    
    # Make prediction
    prediction = model.predict(data)[0]
    
    # Return result
    result = "Benign" if prediction == 1 else "Malignant"
    return {"prediction": result}