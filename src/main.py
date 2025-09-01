
---

# backend/main.py
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from .ai_provider import AiProvider

load_dotenv()

app = FastAPI(title="FitPlanner - GPT5 Showcase (Backend)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

provider = AiProvider()

class PlanRequest(BaseModel):
    name: str
    age: int
    weight_kg: float
    height_cm: float
    goal: str
    experience_level: str = "beginner"

@app.get("/")
def health():
    return {"status": "ok", "provider": provider.name}

@app.post("/api/generate-plan")
async def generate_plan(req: PlanRequest):
    try:
        prompt = req.dict()
        plan = await provider.generate_plan(prompt)
        return {"ok": True, "plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
