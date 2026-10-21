from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import math
import time

app = FastAPI(
    title="AERO-STENT Clinical Telemetry API",
    description="Backend microservice handling Bluetooth/MQTT clinical telemetry streams, patient airway pressure waveforms, and session compliance logging.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DeviceTelemetry(BaseModel):
    device_id: str
    battery_level_pct: float
    current_pressure_cmH2O: float
    drug_remaining_mL: float
    piezo_frequency_kHz: float
    pep_resistance_cmH2O: float
    breath_count: int
    is_barotrauma_alarm: bool

current_device_state = {
    "device_id": "AEROSTENT-PRO-01",
    "battery_level_pct": 92.4,
    "current_pressure_cmH2O": 0.0,
    "drug_remaining_mL": 4.18,
    "piezo_frequency_kHz": 110.0,
    "pep_resistance_cmH2O": 10.0,
    "breath_count": 48,
    "is_barotrauma_alarm": False
}

@app.get("/")
def read_root():
    return {
        "system": "AERO-STENT Telemetry Backend",
        "status": "ONLINE",
        "version": "1.0.0",
        "team": "TECHTONICS | IIT Indore"
    }

@app.get("/api/telemetry")
def get_telemetry():
    return current_device_state

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await websocket.accept()
    t = 0.0
    try:
        while True:
            t += 0.1
            cycle = t % 4.0
            if cycle < 1.4:
                pressure = -0.6 * math.sin((cycle / 1.4) * math.pi)
                phase = "INHALATION_NEBULIZING"
            elif cycle < 3.6:
                pressure = 10.0 * math.sin(((cycle - 1.4) / 2.2) * math.pi)
                phase = "EXHALATION_PEP_STENTING"
            else:
                pressure = 0.0
                phase = "RESPIRATORY_PAUSE"

            payload = {
                "timestamp": time.time(),
                "pressure_cmH2O": round(pressure, 2),
                "phase": phase,
                "drug_remaining_mL": round(max(0.0, 4.2 - (t * 0.002)), 2),
                "frequency_kHz": 110.0,
                "alarm": False
            }
            await websocket.send_json(payload)
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pass
