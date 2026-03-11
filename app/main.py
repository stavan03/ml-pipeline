from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import joblib
import numpy as np
import json
from datetime import datetime

# Load the saved model
model = joblib.load("models/model.pkl")

# Create the API
app = FastAPI()

# In-memory storage for predictions
prediction_log = []

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
    
    # Log the prediction
    prediction_log.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "result": result
    })
    
    return {"prediction": result}

@app.get("/stats")
def stats():
    total = len(prediction_log)
    malignant = sum(1 for p in prediction_log if p["result"] == "Malignant")
    benign = sum(1 for p in prediction_log if p["result"] == "Benign")
    return {
        "total_predictions": total,
        "malignant": malignant,
        "benign": benign,
        "log": prediction_log
    }

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    total = len(prediction_log)
    malignant = sum(1 for p in prediction_log if p["result"] == "Malignant")
    benign = sum(1 for p in prediction_log if p["result"] == "Benign")

    rows = "".join(
        f"<tr><td>{p['timestamp']}</td><td>{p['result']}</td></tr>"
        for p in prediction_log
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ML Pipeline Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f4f4f4; }}
            h1 {{ color: #333; }}
            .cards {{ display: flex; gap: 20px; margin: 20px 0; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; min-width: 150px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .card h2 {{ margin: 0; font-size: 2em; color: #444; }}
            .card p {{ margin: 5px 0 0; color: #888; }}
            table {{ background: white; border-collapse: collapse; width: 100%; max-width: 600px; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            th {{ background: #4a90d9; color: white; padding: 12px; text-align: left; }}
            td {{ padding: 10px 12px; border-bottom: 1px solid #eee; }}
            tr:last-child td {{ border-bottom: none; }}
        </style>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h1>🧠 ML Pipeline Dashboard</h1>
        <div class="cards">
            <div class="card"><h2>{total}</h2><p>Total Predictions</p></div>
            <div class="card"><h2>{malignant}</h2><p>Malignant</p></div>
            <div class="card"><h2>{benign}</h2><p>Benign</p></div>
        </div>
        <h2>Prediction Log</h2>
        <table>
            <tr><th>Timestamp</th><th>Result</th></tr>
            {rows}
        </table>
    </body>
    </html>
    """
    return html