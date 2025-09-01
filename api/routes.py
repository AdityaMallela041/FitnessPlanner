from fastapi import APIRouter, HTTPException, Depends
from models.user_model import PlanRequest, UserProfile
from models.plan_model import PlanResponse, FitnessPlan
from templates.generate_plan import PromptTemplates
from llm_models.gemini import GeminiModel
from llm_models.anthropic import AnthropicModel
from llm_models.groq import GroqModel
import logging
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter()

# Model instances
gemini_model = None
anthropic_model = None
groq_model = None

def get_gemini_model():
    global gemini_model
    if gemini_model is None:
        try:
            gemini_model = GeminiModel()
        except ValueError as e:
            logger.error(f"Failed to initialize Gemini model: {str(e)}")
            raise HTTPException(status_code=500, detail="Gemini model not available")
    return gemini_model

def get_anthropic_model():
    global anthropic_model
    if anthropic_model is None:
        try:
            anthropic_model = AnthropicModel()
        except ValueError as e:
            logger.error(f"Failed to initialize Anthropic model: {str(e)}")
            raise HTTPException(status_code=500, detail="Anthropic model not available")
    return anthropic_model

def get_groq_model():
    global groq_model
    if groq_model is None:
        try:
            groq_model = GroqModel()
        except ValueError as e:
            logger.error(f"Failed to initialize Groq model: {str(e)}")
            raise HTTPException(status_code=500, detail="Groq model not available")
    return groq_model

def create_fallback_response(user_profile: UserProfile) -> FitnessPlan:
    """Create a basic fallback response when AI models fail"""
    return FitnessPlan(
        meal_plan={
            "goal": f"Support {user_profile.goal.lower()} goals",
            "calorie_target": "Calculate based on BMR and activity level",
            "macronutrient_breakdown": {
                "protein": "25-30%",
                "carbohydrates": "40-50%", 
                "fats": "25-30%"
            },
            "meal_frequency": "3 main meals + 2 snacks",
            "sample_meals": {
                "breakfast": ["Oatmeal with protein powder and berries", "Greek yogurt with nuts and honey"],
                "lunch": ["Grilled chicken with quinoa and vegetables", "Salmon salad with mixed greens"],
                "dinner": ["Lean beef with sweet potato and broccoli", "Tofu stir-fry with brown rice"],
                "snacks": ["Apple with almond butter", "Protein shake with banana"]
            },
            "nutrition_tips": [
                "Stay hydrated with 8-10 glasses of water daily",
                "Eat protein with every meal",
                "Include colorful vegetables for micronutrients"
            ],
            "supplements": ["Whey protein", "Multivitamin", "Omega-3"]
        },
        workout_plan={
            "goal": f"Support {user_profile.goal.lower()} through structured training",
            "frequency": f"{user_profile.workout_days} days per week",
            "split": user_profile.workout_split,
            "weekly_schedule": [
                {
                    "day_name": "Day 1",
                    "focus": "Upper Body",
                    "exercises": [
                        {
                            "name": "Push-ups",
                            "sets": "3",
                            "reps": "8-12",
                            "rest": "60 seconds",
                            "notes": "Modify on knees if needed"
                        },
                        {
                            "name": "Squats",
                            "sets": "3", 
                            "reps": "12-15",
                            "rest": "60 seconds",
                            "notes": "Focus on proper form"
                        }
                    ],
                    "duration": f"{user_profile.time_per_session} minutes",
                    "warm_up": ["5 minutes light cardio", "Dynamic stretching"],
                    "cool_down": ["5 minutes walking", "Static stretching"]
                }
            ],
            "progression_notes": [
                "Increase weight/reps when you can complete all sets easily",
                "Track your workouts for consistent progress"
            ],
            "safety_tips": [
                "Always warm up before exercising",
                "Stop if you feel pain or discomfort"
            ]
        },
        general_recommendations=[
            "Get 7-9 hours of quality sleep",
            "Manage stress through relaxation techniques",
            "Be consistent with your routine"
        ],
        progress_tracking={
            "weight": "Weekly weigh-ins at the same time",
            "measurements": "Monthly body measurements",
            "performance": "Track weights, reps, and workout duration"
        }
    )

@router.post("/generate-plan", response_model=PlanResponse)
async def generate_plan_gemini(request: PlanRequest, model: GeminiModel = Depends(get_gemini_model)):
    try:
        prompt = PromptTemplates.generate_fitness_plan_prompt(request.user_profile)
        result = await model.generate_plan(prompt)
        
        if result:
            return PlanResponse(
                status="200",
                message="Plan generated successfully",
                data=FitnessPlan(**result)
            )
        else:
            # Fallback response
            fallback_data = create_fallback_response(request.user_profile)
            return PlanResponse(
                status="200",
                message="Plan generated with fallback data",
                data=fallback_data
            )
            
    except Exception as e:
        logger.error(f"Error in generate_plan_gemini: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-plan-anthropic", response_model=PlanResponse)
async def generate_plan_anthropic(request: PlanRequest, model: AnthropicModel = Depends(get_anthropic_model)):
    try:
        prompt = PromptTemplates.generate_fitness_plan_prompt(request.user_profile)
        result = await model.generate_plan(prompt)
        
        if result:
            return PlanResponse(
                status="200",
                message="Plan generated successfully with Anthropic",
                data=FitnessPlan(**result)
            )
        else:
            fallback_data = create_fallback_response(request.user_profile)
            return PlanResponse(
                status="200", 
                message="Plan generated with fallback data",
                data=fallback_data
            )
            
    except Exception as e:
        logger.error(f"Error in generate_plan_anthropic: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-plan-groq", response_model=PlanResponse)
async def generate_plan_groq(request: PlanRequest, model: GroqModel = Depends(get_groq_model)):
    try:
        prompt = PromptTemplates.generate_fitness_plan_prompt(request.user_profile)
        result = await model.generate_plan(prompt)
        
        if result:
            return PlanResponse(
                status="200",
                message="Plan generated successfully with Groq",
                data=FitnessPlan(**result)
            )
        else:
            fallback_data = create_fallback_response(request.user_profile)
            return PlanResponse(
                status="200",
                message="Plan generated with fallback data", 
                data=fallback_data
            )
            
    except Exception as e:
        logger.error(f"Error in generate_plan_groq: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "FitPlanner API is running"}
