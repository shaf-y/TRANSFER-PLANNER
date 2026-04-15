import os
import json
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from PIL import Image
import io

app = FastAPI(title="Vision Transfer Plan API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload-plan")
async def extract_and_plan(file: UploadFile = File(...)):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: GEMINI_API_KEY environment variable is not set. Please add it to your local environment or Vercel settings."
        )

    genai.configure(api_key=api_key)
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Dynamically select the best available model for this specific API key to eliminate 404s
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        target_model_name = None
        for pref in ["models/gemini-1.5-pro-latest", "models/gemini-1.5-flash-latest", "models/gemini-1.5-pro", "models/gemini-1.5-flash", "models/gemini-2.5-flash", "models/gemini-pro-vision"]:
            if pref in available_models:
                target_model_name = pref
                break
                
        if not target_model_name:
            target_model_name = available_models[0] if available_models else 'gemini-1.5-pro'
            
        # Strip "models/" if present for the GenerativeModel constructor
        clean_model_name = target_model_name.replace('models/', '')
        model = genai.GenerativeModel(clean_model_name)
        
        prompt = """
        You are an expert academic advisor for De Anza College transfers to UC Berkeley.
        I am giving you an image showing a set of classes a student intends to take. The image might have the classes distributed loosely across quarters, or just a list.
        YOUR TASK: Look at these exact courses from the image. Identify them. Estimate their typical unit values and difficulty (out of 10).
        Then, rigorously optimize them into exactly 4 Quarters (Summer, Fall, Winter, Spring).
        CRITICAL CONSTRAINTS: 
        1. Ensure sequencing logic is roughly maintained (A before B before C).
        2. Summer absolute maximum is 15.0 units. Fall/Winter/Spring absolute maximum is 21.5 units each. Check your math rigorously!
        
        You MUST output ONLY valid JSON using the following schema (NO markdown blocks, NO backticks, NO text outside the JSON).
        {
          "plan": [
            {
              "term": "Summer 2026",
              "total_units": <float>,
              "max_units": 15.0,
              "difficulty_score": <int>,
              "courses": [
                {
                  "id": "COURSE ID",
                  "name": "Course Name",
                  "units": <float>,
                  "difficulty": <int>
                }
              ]
            },
            ... Fall, Winter, Spring
          ]
        }
        """
        
        response = model.generate_content([prompt, image])
        
        raw_text = response.text.strip()
        # Clean up if the LLM wraps it in markdown despite instructions
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "", 1).strip()
        if raw_text.endswith("```"):
            raw_text = raw_text[::-1].replace("```", "", 1)[::-1].strip()

        parsed_json = json.loads(raw_text)
        return parsed_json
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI parsing failure. Try uploading the image again.")
    except Exception as e:
        try:
            available_models = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
        except Exception:
            available_models = ["Failed to fetch models"]
        raise HTTPException(status_code=500, detail=f"Model gemini-1.5-pro Error: {str(e)} | Available models for your API key: {available_models}")


@app.get("/")
def read_root():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return FileResponse(os.path.join(base_dir, "static/index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
