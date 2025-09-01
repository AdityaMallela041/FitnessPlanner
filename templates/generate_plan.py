from models.user_model import UserProfile

class PromptTemplates:
    @staticmethod
    def generate_fitness_plan_prompt(user_profile: UserProfile) -> str:
        return f"""
You are an expert fitness and nutrition coach. Create a comprehensive, personalized fitness plan for the following user profile:

**User Profile:**
- Age: {user_profile.age} years
- Gender: {user_profile.gender}
- Height: {user_profile.height} cm
- Weight: {user_profile.weight} kg
- Activity Level: {user_profile.activity_level}
- Fitness Goal: {user_profile.goal}
- Target Weight: {user_profile.goal_weight} kg (if specified)

**Nutrition Preferences:**
- Meal Preference: {user_profile.meal_preference}
- Meal Type: {user_profile.meal_type}
- Allergies: {user_profile.allergies}
- Medical Conditions: {user_profile.medical_conditions}
- Food Restrictions: {user_profile.food_restrictions}

**Workout Preferences:**
- Workout Days: {user_profile.workout_days} days per week
- Location: {user_profile.workout_location}
- Split: {user_profile.workout_split}
- Experience: {user_profile.workout_experience}
- Equipment: {user_profile.equipment_available}
- Session Duration: {user_profile.time_per_session} minutes

**Requirements:**
1. Create a detailed meal plan with:
   - Daily calorie target based on BMR and activity level
   - Macronutrient breakdown (protein, carbs, fats)
   - Sample meals for each meal time
   - Nutrition tips and supplement recommendations

2. Create a comprehensive workout plan with:
   - Weekly schedule with specific days
   - Exercise names, sets, reps, and rest periods
   - Warm-up and cool-down routines
   - Progression guidelines and safety tips

3. Provide general recommendations for:
   - Progress tracking methods
   - Lifestyle modifications
   - Recovery strategies

**Output Format:**
Provide the response in a structured JSON format that matches this schema:
{{
  "meal_plan": {{
    "goal": "specific goal description",
    "calorie_target": "daily calorie range",
    "macronutrient_breakdown": {{
      "protein": "percentage or grams",
      "carbohydrates": "percentage or grams", 
      "fats": "percentage or grams"
    }},
    "meal_frequency": "meal timing strategy",
    "sample_meals": {{
      "breakfast": ["meal option 1", "meal option 2"],
      "lunch": ["meal option 1", "meal option 2"],
      "dinner": ["meal option 1", "meal option 2"],
      "snacks": ["snack option 1", "snack option 2"]
    }},
    "nutrition_tips": ["tip 1", "tip 2", "tip 3"],
    "supplements": ["supplement 1", "supplement 2"]
  }},
  "workout_plan": {{
    "goal": "workout goal description",
    "frequency": "days per week",
    "split": "workout split type",
    "weekly_schedule": [
      {{
        "day_name": "Day 1",
        "focus": "muscle groups or type",
        "exercises": [
          {{
            "name": "Exercise Name",
            "sets": "number of sets",
            "reps": "repetition range",
            "rest": "rest period",
            "notes": "form cues or modifications"
          }}
        ],
        "duration": "estimated time",
        "warm_up": ["warm-up exercise 1", "warm-up exercise 2"],
        "cool_down": ["cool-down exercise 1", "cool-down exercise 2"]
      }}
    ],
    "progression_notes": ["progression tip 1", "progression tip 2"],
    "safety_tips": ["safety tip 1", "safety tip 2"]
  }},
  "general_recommendations": ["recommendation 1", "recommendation 2"],
  "progress_tracking": {{
    "weight": "tracking frequency and method",
    "measurements": "what to measure and when",
    "performance": "how to track workout progress"
  }}
}}

Make sure the plan is realistic, safe, and tailored to the user's specific needs and constraints.
"""

    @staticmethod
    def validate_plan_prompt(plan_text: str) -> str:
        return f"""
Validate and improve the following fitness plan. Ensure it's:
1. Scientifically accurate
2. Safe for the user
3. Realistic and achievable
4. Properly formatted as JSON

Plan to validate:
{plan_text}

If there are any issues, provide the corrected version. If it's good, return it as-is.
"""
