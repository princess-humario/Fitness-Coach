from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
import time
import logging
from models import AdviceRequest, AdviceResponse, Config
from prompt_templates import PromptSelector
from moderation import FitnessModerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Fitness Coach AI",
    description="Get personalized fitness advice powered by AI",
    version="1.0.0"
)

Config.validate_api_key()
client = OpenAI(api_key=Config.OPENAI_API_KEY)

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fitness Coach AI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 500px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .header h1 {
            color: #333;
            margin-bottom: 0.5rem;
            font-size: 2rem;
        }
        
        .header p {
            color: #666;
            font-size: 1.1rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: #333;
        }
        
        select, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e1e1;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        
        select:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        
        .submit-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
        }
        
        .submit-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .result {
            margin-top: 2rem;
            padding: 1.5rem;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            display: none;
        }
        
        .result h3 {
            color: #333;
            margin-bottom: 1rem;
        }
        
        .advice-text {
            line-height: 1.6;
            color: #555;
            margin-bottom: 1rem;
        }
        
        .metrics {
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
            color: #666;
            border-top: 1px solid #eee;
            padding-top: 1rem;
        }
        
        .metric {
            text-align: center;
        }
        
        .metric-value {
            font-weight: bold;
            color: #667eea;
        }
        
        .loading {
            text-align: center;
            color: #667eea;
            font-weight: 600;
        }
        
        .error {
            background: #fee;
            border-left-color: #e74c3c;
            color: #c0392b;
        }

        .api-info {
            text-align: center;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
        }
        
        .api-info a {
            color: #667eea;
            text-decoration: none;
            margin: 0 1rem;
        }
        
        .api-info a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Fitness Coach AI</h1>
        </div>
        
        <form id="fitness-form">
            <div class="form-group">
                <label for="goal">What's your fitness goal?</label>
                <select id="goal" required>
                    <option value="">Choose your goal...</option>
                    <option value="lose weight">Lose Weight</option>
                    <option value="gain muscle">Gain Muscle</option>
                    <option value="general fitness">General Fitness</option>
                    <option value="endurance">Build Endurance</option>
                    <option value="strength">Increase Strength</option>
                    <option value="flexibility">Improve Flexibility</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="fitness_level">What's your fitness level?</label>
                <select id="fitness_level" required>
                    <option value="">Choose your level...</option>
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="question">What would you like to know?</label>
                <textarea 
                    id="question" 
                    placeholder="e.g., What should I eat after a workout? How many times should I exercise per week?"
                    required
                ></textarea>
            </div>
            
            <button type="submit" class="submit-btn">Get My Fitness Advice</button>
        </form>
        
        <div id="result" class="result">
            <h3>Your Personalized Advice</h3>
            <div id="advice-text" class="advice-text"></div>
            <div id="metrics" class="metrics">
                <div class="metric">
                    <div class="metric-value" id="safety-status"></div>
                    <div>Safety Check</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="response-time">0.0s</div>
                    <div>Response Time</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="word-count">0</div>
                    <div>Words</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('fitness-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const button = e.target.querySelector('.submit-btn');
            const resultDiv = document.getElementById('result');
            const adviceText = document.getElementById('advice-text');
            
            // Show loading state
            button.disabled = true;
            button.textContent = 'Getting your advice...';
            resultDiv.style.display = 'block';
            resultDiv.className = 'result loading';
            adviceText.textContent = 'AI is thinking about your question...';
            
            const requestData = {
                goal: document.getElementById('goal').value,
                fitness_level: document.getElementById('fitness_level').value,
                question: document.getElementById('question').value
            };
            
            try {
                const response = await fetch('/advise', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestData)
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                // Show results
                resultDiv.className = 'result';
                adviceText.textContent = data.advice;
                
                // Update metrics
                document.getElementById('safety-status').textContent = data.moderation_passed ? '✅' : '⚠️';
                document.getElementById('response-time').textContent = `${data.response_time?.toFixed(1)}s`;
                document.getElementById('word-count').textContent = data.word_count;
                
            } catch (error) {
                resultDiv.className = 'result error';
                adviceText.textContent = `Sorry, something went wrong: ${error.message}`;
            }
            
            // Reset button
            button.disabled = false;
            button.textContent = 'Get My Fitness Advice';
        });
    </script>
</body>
</html>
    """)

@app.post("/advise")
async def get_fitness_advice(request: AdviceRequest) -> AdviceResponse:
    start_time = time.time()
    
    try:
        logger.info(f"Processing request: {request.goal} | {request.fitness_level}")
        
        prompt = PromptSelector.select_prompt_strategy(
            goal=request.goal,
            fitness_level=request.fitness_level,
            question=request.question
        )
        
        response = client.chat.completions.create(
            model=Config.MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=Config.MAX_TOKENS,
            temperature=Config.TEMPERATURE
        )
        
        advice = response.choices[0].message.content.strip()
        
        moderation_result = FitnessModerator.moderate_advice(advice)
        
        if not moderation_result["passed"]:
            logger.warning(f"Moderation failed: {moderation_result['reason']}")
            advice = FitnessModerator.get_safe_fallback_advice(request.goal)
        
        response_time = time.time() - start_time
        word_count = len(advice.split())
        
        logger.info(f"Advice generated successfully in {response_time:.2f}s")
        
        return AdviceResponse(
            advice=advice,
            moderation_passed=moderation_result["passed"],
            response_time=response_time,
            word_count=word_count
        )
        
    except Exception as e:
        logger.error(f"Error generating advice: {str(e)}")
        
        response_time = time.time() - start_time
        fallback_advice = FitnessModerator.get_safe_fallback_advice(request.goal)
        
        return AdviceResponse(
            advice=fallback_advice + f" (Error: {str(e)})",
            moderation_passed=False,
            response_time=response_time,
            word_count=len(fallback_advice.split())
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "fitness-coach-ai",
        "endpoints": {
            "home": "/",
            "advice": "/advise",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
