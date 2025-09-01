from pydantic import BaseModel, Field
from typing import Optional, Literal

class UserProfile(BaseModel):
    # Basic Info
    age: int = Field(..., ge=13, le=100, description="Age in years")
    gender: Literal["Male", "Female", "Other"] = Field(..., description="Gender")
    height: float = Field(..., ge=100, le=250, description="Height in cm")
    weight: float = Field(..., ge=30, le=300, description="Weight in kg")
    
    # Activity & Goals
    activity_level: Literal[
        "Sedentary", 
        "Lightly Active", 
        "Moderately Active", 
        "Very Active", 
        "Extremely Active"
    ] = Field(..., description="Activity level")
    
    goal: Literal[
        "Weight Loss", 
        "Weight Gain", 
        "Muscle Building", 
        "Lean Bulk", 
        "Maintenance", 
        "Athletic Performance"
    ] = Field(..., description="Fitness goal")
    
    goal_weight: Optional[float] = Field(None, ge=30, le=300, description="Target weight in kg")
    
    # Nutrition Preferences
    meal_preference: Literal[
        "Vegetarian", 
        "Non-Vegetarian", 
        "Vegan", 
        "Pescatarian", 
        "Keto", 
        "Paleo"
    ] = Field(..., description="Dietary preference")
    
    meal_type: Literal[
        "High Protein", 
        "Balanced", 
        "Low Carb", 
        "High Carb", 
        "Mediterranean"
    ] = Field(..., description="Meal type preference")
    
    allergies: Optional[str] = Field("N/A", description="Food allergies")
    medical_conditions: Optional[str] = Field("N/A", description="Medical conditions")
    food_restrictions: Optional[str] = Field("N/A", description="Food restrictions")
    
    # Workout Preferences
    workout_days: int = Field(..., ge=1, le=7, description="Days per week for workout")
    workout_location: Literal["Home", "Gym", "Outdoor", "Mixed"] = Field(..., description="Workout location")
    workout_split: Literal[
        "Full Body", 
        "Upper/Lower", 
        "Push Pull Legs", 
        "Body Part Split", 
        "HIIT", 
        "Functional"
    ] = Field(..., description="Workout split type")
    
    workout_experience: Literal[
        "Beginner", 
        "Amateur", 
        "Intermediate", 
        "Advanced", 
        "Expert"
    ] = Field(..., description="Workout experience level")
    
    equipment_available: Optional[str] = Field("Basic gym equipment", description="Available equipment")
    time_per_session: Optional[int] = Field(60, ge=15, le=180, description="Minutes per workout session")

class PlanRequest(BaseModel):
    user_profile: UserProfile
    ai_provider: Literal["gemini", "anthropic", "groq"] = Field("gemini", description="AI provider to use")
