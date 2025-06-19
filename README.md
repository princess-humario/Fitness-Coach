# Fitness-Coach-API
## Prerequisites

- Python 3.10+
- OpenAI API key

## Setup

- Virtual environment: python -m venv .venv
- venv\Scripts\activate
- Installing packages: pip install fastapi uvicorn openai python-dotenv
- API key: Add your API key in a separate .env file. This will be called automatically in the models.py file with load_dotenv() function
- Run: Run with python main.py in the terminal

## Example API calls

### Weight Loss advice
curl -X POST "http://localhost:8000/advise" \
-H "Content-Type: application/json" \
-d '{
  "goal": "lose weight",
  "fitness_level": "beginner",
  "question": "How many calories should I eat daily?"
}'

### Muscle Building
curl -X POST "http://localhost:8000/advise" \
-H "Content-Type: application/json" \
-d '{
  "goal": "gain muscle",
  "fitness_level": "intermediate",
  "question": "Best protein sources for muscle growth?"
}'

### General fitness
curl -X POST "http://localhost:8000/advise" \
-H "Content-Type: application/json" \
-d '{
  "goal": "general fitness",
  "fitness_level": "advanced",
  "question": "How to create a balanced workout routine?"
}'

## Prompt engineering comparison

### Tone changes
- Before: Casual, generic responses
- After: Professional, expert-level advice with confident delivery

### Safety changes
- Before: No safety check before
- After: Does not give harmful advice








