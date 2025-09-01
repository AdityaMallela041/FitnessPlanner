# FitPlanner - LlamaIndex Edition

A comprehensive fitness planning application that generates personalized nutrition and workout plans using multiple AI providers through LlamaIndex.

## 🚀 Features

- **Multiple AI Providers**: Support for Gemini, Anthropic (Claude), and Groq (Llama models)
- **LlamaIndex Integration**: Advanced AI orchestration for better performance
- **Personalized Plans**: Custom meal and workout plans based on user profiles
- **Modern UI**: Beautiful Streamlit interface with enhanced user experience
- **REST API**: FastAPI backend for flexible integration

## 🏗️ Architecture

The application is built with:
- **Backend**: FastAPI with LlamaIndex for AI model integration
- **Frontend**: Streamlit for interactive user interface
- **AI Models**: 
  - Google Gemini Pro
  - Anthropic Claude 3 Opus
  - Groq Llama models

## 📋 Prerequisites

- Python 3.8+
- API keys for the AI providers you want to use:
  - Google AI API key (for Gemini)
  - Anthropic API key (for Claude)
  - Groq API key (for Llama models)

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd fitplan-streamlit
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp env.example .env
```

Edit `.env` and add your API keys:
```
GOOGLE_API_KEY=your_google_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

## 🚀 Usage

### Start the FastAPI Backend

```bash
python main.py
```

The API will be available at `http://localhost:5000`

### Available Endpoints

- `POST /api/generate-plan` - Generate plan using Gemini
- `POST /api/generate-plan-anthropic` - Generate plan using Anthropic Claude
- `POST /api/generate-plan-groq` - Generate plan using Groq Llama

### Start the Streamlit Frontend

```bash
streamlit run streamlit/streamlit_app.py
```

The web app will be available at `http://localhost:8501`

## 📝 API Usage

### Request Format

```json
{
  "age": 25,
  "gender": "Male",
  "height": 175,
  "weight": 70.0,
  "activity_level": "Moderately Active",
  "goal": "Lean Bulk",
  "goal_weight": 75.0,
  "meal_preference": "Non-Vegetarian",
  "meal_type": "High Protein",
  "allergies": "N/A",
  "medical_conditions": "N/A",
  "food_restrictions": "N/A",
  "workout_days": 4,
  "workout_location": "Gym",
  "workout_split": "Push Pull Legs",
  "workout_experience": "Amateur"
}
```

### Response Format

```json
{
  "status": "200",
  "data": {
    "meal_plan": {
      "goal": "Build lean muscle mass",
      "calorie_target": "2500-2800 calories per day",
      "macronutrient_breakdown": {
        "protein": "30%",
        "carbohydrates": "40%", 
        "fats": "30%"
      },
      "meal_frequency": "3 main meals + 2 snacks",
      "sample_meals": {
        "breakfast": ["Oatmeal with protein powder", "Greek yogurt with berries"],
        "lunch": ["Grilled chicken with quinoa", "Salmon with sweet potato"],
        "dinner": ["Lean beef with brown rice", "Turkey with vegetables"]
      }
    },
    "workout_plan": {
      "goal": "Build lean muscle and strength",
      "frequency": "4 days per week",
      "split": "Push Pull Legs",
      "exercises": {
        "push": ["Bench Press", "Shoulder Press", "Tricep Dips"],
        "pull": ["Pull-ups", "Rows", "Bicep Curls"],
        "legs": ["Squats", "Deadlifts", "Lunges"]
      }
    }
  }
}
```

## 🏗️ Project Structure

```
fitplan-streamlit/
├── api/
│   ├── __init__.py
│   └── routes.py              # FastAPI routes with LlamaIndex integration
├── config/
│   ├── __init__.py
│   └── env_config.py          # Environment configuration
├── llm_models/
│   ├── __init__.py
│   ├── anthropic.py           # Anthropic Claude model
│   ├── gemini.py              # Google Gemini model
│   └── groq.py                # Groq Llama model
├── models/
│   ├── __init__.py
│   ├── plan_model.py          # Pydantic models for plans
│   └── user_model.py          # User input model
├── streamlit/
│   └── streamlit_app.py       # Streamlit frontend
├── templates/
│   ├── __init__.py
│   └── generate_plan.py       # Prompt templates
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── env.example               # Environment variables template
└── README.md                 # This file
```

## 🔧 Configuration

### AI Model Configuration

Each AI provider can be configured in their respective files:

- **Gemini**: `llm_models/gemini.py`
- **Anthropic**: `llm_models/anthropic.py`  
- **Groq**: `llm_models/groq.py`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI API key for Gemini | For Gemini support |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude | For Claude support |
| `GROQ_API_KEY` | Groq API key for Llama models | For Groq support |

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

2. **API connection errors**: Ensure the FastAPI server is running on port 5000

3. **AI model errors**: Check that your API keys are correctly set in the `.env` file

4. **Response parsing errors**: The application includes fallback responses for parsing issues

### Debug Mode

To run with debug logging:

```bash
python main.py --log-level debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LlamaIndex](https://llamaindex.ai/) for the excellent AI orchestration framework
- [FastAPI](https://fastapi.tiangolo.com/) for the robust API framework
- [Streamlit](https://streamlit.io/) for the beautiful UI framework
- AI providers: Google (Gemini), Anthropic (Claude), and Groq (Llama)
