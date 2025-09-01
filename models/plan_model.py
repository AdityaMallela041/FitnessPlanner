from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class MacronutrientBreakdown(BaseModel):
    protein: str
    carbohydrates: str
    fats: str
    fiber: Optional[str] = None

class MealPlan(BaseModel):
    goal: str
    calorie_target: str
    macronutrient_breakdown: MacronutrientBreakdown
    meal_frequency: str
    sample_meals: Dict[str, List[str]]
    nutrition_tips: Optional[List[str]] = []
    supplements: Optional[List[str]] = []

class Exercise(BaseModel):
    name: str
    sets: str
    reps: str
    rest: Optional[str] = None
    notes: Optional[str] = None

class WorkoutDay(BaseModel):
    day_name: str
    focus: str
    exercises: List[Exercise]
    duration: Optional[str] = None
    warm_up: Optional[List[str]] = []
    cool_down: Optional[List[str]] = []

class WorkoutPlan(BaseModel):
    goal: str
    frequency: str
    split: str
    weekly_schedule: List[WorkoutDay]
    progression_notes: Optional[List[str]] = []
    safety_tips: Optional[List[str]] = []

class FitnessPlan(BaseModel):
    meal_plan: MealPlan
    workout_plan: WorkoutPlan
    general_recommendations: Optional[List[str]] = []
    progress_tracking: Optional[Dict[str, str]] = {}

class PlanResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[FitnessPlan] = None
    error: Optional[str] = None
