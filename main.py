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
    data = await request.json()
    bpm = data.get("bpm")
    if bpm:
        latest_bpm["value"] = bpm
        print(f"Received BPM: {bpm}")
        return {"status": "ok", "received": bpm}
    else:
        return {"status": "error", "message": "Missing bpm"}


@app.get("/latest-bpm")
def get_latest_bpm():
    if latest_bpm["value"] is None:
        return {"status": "no data yet"}
    return {"bpm": latest_bpm["value"]}
