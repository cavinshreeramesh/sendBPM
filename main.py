from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# In-memory BPM storage
latest_bpm = {"value": None}

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with allowed origins in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/heart-data")
async def receive_bpm(request: Request):
    try:
        data = await request.json()
        bpm = data.get("bpm")
        if bpm is None:
            raise HTTPException(status_code=400, detail="Missing 'bpm' in request")

        latest_bpm["value"] = bpm
        print(f"✅ Received BPM: {bpm}")
        return {"status": "ok", "received": bpm}

    except Exception as e:
        print(f"❌ Error receiving BPM: {e}")
        raise HTTPException(status_code=500, detail="Invalid data format")

@app.get("/latest-bpm")
def get_latest_bpm():
    if latest_bpm["value"] is None:
        return {"status": "no data yet"}
    return {"bpm": latest_bpm["value"]}
