from fastapi import FastAPI
from fastapi.responses import FileResponse
from scheduler import generate_plan
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Optimal Transfer Plan API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/plan")
def get_plan():
    return {"plan": generate_plan()}

@app.get("/")
def read_root():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return FileResponse(os.path.join(base_dir, "static/index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
