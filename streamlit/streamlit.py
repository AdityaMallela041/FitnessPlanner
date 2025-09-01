import streamlit as st
import requests
import json
from typing import Dict, Any
import time

# Page configuration
st.set_page_config(
    page_title="FitPlanner - AI Fitness Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4ECDC4;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #FF6B6B;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #D4F8D4;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28A745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:5000/api"

def make_api_request(endpoint: str, data: Dict[Any, Any]) -> Dict[Any, Any]:
    """Make API request with error handling"""
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return None

def display_meal_plan(meal_plan: Dict[Any, Any]):
    """Display meal plan in a formatted way"""
    st.markdown("### 🍽️ Personalized Meal Plan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Goal:**")
        st.info(meal_plan.get("goal", "Not specified"))
        
        st.markdown("**Daily Calorie Target:**")
        st.success(meal_plan.get("calorie_target", "Not specified"))
        
        st.markdown("**Meal Frequency:**")
        st.info(meal_plan.get("meal_frequency", "Not specified"))
    
    with col2:
        st.markdown("**Macronutrient Breakdown:**")
        macros = meal_plan.get("macronutrient_breakdown", {})
        if macros:
            st.write(f"• Protein: {macros.get('protein', 'N/A')}")
            st.write(f"• Carbohydrates: {macros.get('carbohydrates', 'N/A')}")
            st.write(f"• Fats: {macros.get('fats', 'N/A')}")
    
    # Sample Meals
    st.markdown("**Sample Meals:**")
    sample_meals = meal_plan.get("sample_meals", {})
    
    meal_tabs = st.tabs(["Breakfast", "Lunch", "Dinner", "Snacks"])
    
    for i, (meal_type, tab) in enumerate(zip(["breakfast", "lunch", "dinner", "snacks"], meal_tabs)):
        with tab:
            meals = sample_meals.get(meal_type, [])
            if meals:
                for j, meal in enumerate(meals, 1):
                    st.write(f"{j}. {meal}")
            else:
                st.write("No meals specified for this time.")
    
    # Nutrition Tips
    tips = meal_plan.get("nutrition_tips", [])
    if tips:
        st.markdown("**Nutrition Tips:**")
        for tip in tips:
            st.write(f"• {tip}")
    
    # Supplements
    supplements = meal_plan.get("supplements", [])
    if supplements:
        st.markdown("**Recommended Supplements:**")
        for supplement in supplements:
            st.write(f"• {supplement}")

def display_workout_plan(workout_plan: Dict[Any, Any]):
    """Display workout plan in a formatted way"""
    st.markdown("### 🏋️ Personalized Workout Plan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Goal:**")
        st.info(workout_plan.get("goal", "Not specified"))
    
    with col2:
        st.markdown("**Frequency:**")
        st.success(workout_plan.get("frequency", "Not specified"))
    
    with col3:
        st.markdown("**Split Type:**")
        st.info(workout_plan.get("split", "Not specified"))
    
    # Weekly Schedule
    weekly_schedule = workout_plan.get("weekly_schedule", [])
    if weekly_schedule:
        st.markdown("**Weekly Schedule:**")
        
        for day in weekly_schedule:
            with st.expander(f"{day.get('day_name', 'Day')} - {day.get('focus', 'Focus')}"):
                
                # Duration
                duration = day.get("duration", "N/A")
                st.write(f"**Duration:** {duration}")
                
                # Warm-up
                warm_up = day.get("warm_up", [])
                if warm_up:
                    st.write("**Warm-up:**")
                    for exercise in warm_up:
                        st.write(f"• {exercise}")
                
                # Main Exercises
                exercises = day.get("exercises", [])
                if exercises:
                    st.write("**Exercises:**")
                    exercise_data = []
                    for exercise in exercises:
                        exercise_data.append({
                            "Exercise": exercise.get("name", "N/A"),
                            "Sets": exercise.get("sets", "N/A"),
                            "Reps": exercise.get("reps", "N/A"),
                            "Rest": exercise.get("rest", "N/A"),
                            "Notes": exercise.get("notes", "N/A")
                        })
                    
                    if exercise_data:
                        st.table(exercise_data)
                
                # Cool-down
                cool_down = day.get("cool_down", [])
                if cool_down:
                    st.write("**Cool-down:**")
                    for exercise in cool_down:
                        st.write(f"• {exercise}")
    
    # Progression Notes
    progression_notes = workout_plan.get("progression_notes", [])
    if progression_notes:
        st.markdown("**Progression Guidelines:**")
        for note in progression_notes:
            st.write(f"• {note}")
    
    # Safety Tips
    safety_tips = workout_plan.get("safety_tips", [])
    if safety_tips:
        st.markdown("**Safety Tips:**")
        for tip in safety_tips:
            st.write(f"• {tip}")

def main():
    # Header
    st.markdown('<h1 class="main-header">💪 FitPlanner - AI Fitness Coach</h1>', unsafe_allow_html=True)
    st.markdown("Get personalized nutrition and workout plans powered by AI")
    
    # Sidebar for user input
    with st.sidebar:
        st.markdown('<h2 class="sub-header">Your Profile</h2>', unsafe_allow_html=True)
        
        # Basic Information
        st.markdown("**Basic Information**")
        age = st.number_input("Age", min_value=13, max_value=100, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=175)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)
        
        # Activity & Goals
        st.markdown("**Activity & Goals**")
        activity_level = st.selectbox("Activity Level", [
            "Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"
        ], index=2)
        
        goal = st.selectbox("Fitness Goal", [
            "Weight Loss", "Weight Gain", "Muscle Building", "Lean Bulk", "Maintenance", "Athletic Performance"
        ], index=2)
        
        goal_weight = st.number_input("Goal Weight (kg)", min_value=30.0, max_value=300.0, value=75.0, step=0.1)
        
        # Nutrition Preferences
        st.markdown("**Nutrition Preferences**")
        meal_preference = st.selectbox("Meal Preference", [
            "Vegetarian", "Non-Vegetarian", "Vegan", "Pescatarian", "Keto", "Paleo"
        ], index=1)
        
        meal_type = st.selectbox("Meal Type", [
            "High Protein", "Balanced", "Low Carb", "High Carb", "Mediterranean"
        ])
        
        allergies = st.text_input("Allergies", value="N/A")
        medical_conditions = st.text_input("Medical Conditions", value="N/A")
        food_restrictions = st.text_input("Food Restrictions", value="N/A")
        
        # Workout Preferences
        st.markdown("**Workout Preferences**")
        workout_days = st.number_input("Workout Days per Week", min_value=1, max_value=7, value=4)
        workout_location = st.selectbox("Workout Location", ["Home", "Gym", "Outdoor", "Mixed"], index=1)
        workout_split = st.selectbox("Workout Split", [
            "Full Body", "Upper/Lower", "Push Pull Legs", "Body Part Split", "HIIT", "Functional"
        ], index=2)
        
        workout_experience = st.selectbox("Experience Level", [
            "Beginner", "Amateur", "Intermediate", "Advanced", "Expert"
        ], index=1)
        
        equipment_available = st.text_input("Available Equipment", value="Basic gym equipment")
        time_per_session = st.number_input("Minutes per Session", min_value=15, max_value=180, value=60)
        
        # AI Provider Selection
        st.markdown("**AI Provider**")
        ai_provider = st.selectbox("Choose AI Model", ["gemini", "anthropic", "groq"])
        
        # Generate Plan Button
        generate_button = st.button("🚀 Generate My Fitness Plan", type="primary")
    
    # Main content area
    if generate_button:
        # Prepare user profile data
        user_profile = {
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "activity_level": activity_level,
            "goal": goal,
            "goal_weight": goal_weight,
            "meal_preference": meal_preference,
            "meal_type": meal_type,
            "allergies": allergies,
            "medical_conditions": medical_conditions,
            "food_restrictions": food_restrictions,
            "workout_days": workout_days,
            "workout_location": workout_location,
            "workout_split": workout_split,
            "workout_experience": workout_experience,
            "equipment_available": equipment_available,
            "time_per_session": time_per_session
        }
        
        request_data = {
            "user_profile": user_profile,
            "ai_provider": ai_provider
        }
        
        # Determine endpoint based on AI provider
        endpoint_map = {
            "gemini": "/generate-plan",
            "anthropic": "/generate-plan-anthropic", 
            "groq": "/generate-plan-groq"
        }
        
        endpoint = endpoint_map.get(ai_provider, "/generate-plan")
        
        # Show loading spinner
        with st.spinner(f"Generating your personalized fitness plan using {ai_provider.title()}..."):
            response = make_api_request(endpoint, request_data)
        
        if response and response.get("status") == "200":
            st.markdown('<div class="success-box">✅ Your personalized fitness plan has been generated!</div>', unsafe_allow_html=True)
            
            plan_data = response.get("data")
            if plan_data:
                # Display meal plan
                meal_plan = plan_data.get("meal_plan")
                if meal_plan:
                    display_meal_plan(meal_plan)
                
                st.markdown("---")
                
                # Display workout plan
                workout_plan = plan_data.get("workout_plan")
                if workout_plan:
                    display_workout_plan(workout_plan)
                
                st.markdown("---")
                
                # General Recommendations
                general_recommendations = plan_data.get("general_recommendations", [])
                if general_recommendations:
                    st.markdown("### 💡 General Recommendations")
                    for rec in general_recommendations:
                        st.write(f"• {rec}")
                
                # Progress Tracking
                progress_tracking = plan_data.get("progress_tracking", {})
                if progress_tracking:
                    st.markdown("### 📊 Progress Tracking")
                    for key, value in progress_tracking.items():
                        st.write(f"**{key.title()}:** {value}")
                
                # Download option
                st.markdown("---")
                st.markdown("### 📥 Export Your Plan")
                
                plan_json = json.dumps(plan_data, indent=2)
                st.download_button(
                    label="Download Plan as JSON",
                    data=plan_json,
                    file_name="my_fitness_plan.json",
                    mime="application/json"
                )
            
        else:
            st.error("Failed to generate fitness plan. Please try again or check your API configuration.")
    
    else:
        # Welcome message and instructions
        st.markdown("### Welcome to FitPlanner! 🎯")
        st.write("""
        **Get started by filling out your profile in the sidebar:**
        
        1. **Basic Information** - Your age, gender, height, and weight
        2. **Activity & Goals** - Your current activity level and fitness goals
        3. **Nutrition Preferences** - Dietary preferences, allergies, and restrictions
        4. **Workout Preferences** - Training frequency, location, and experience level
        5. **AI Provider** - Choose your preferred AI model for generating the plan
        
        Once you've completed your profile, click the **"Generate My Fitness Plan"** button to get your personalized nutrition and workout plan!
        """)
        
        # Feature highlights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card"><h4>🤖 AI-Powered</h4><p>Multiple AI models including Gemini, Claude, and Llama</p></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card"><h4>🎯 Personalized</h4><p>Plans tailored to your specific goals and preferences</p></div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card"><h4>📈 Comprehensive</h4><p>Complete nutrition and workout guidance</p></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
