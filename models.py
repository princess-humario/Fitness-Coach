from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import os
from dotenv import load_dotenv

# Please make sure you have uploaded the API key in another file. Personally im not a fan of putting API key directly in code. I like to keep
#it safe in a separate file. Almost all the online youtube tutorials follow this practice and as a result I have also adopted this habit. 
load_dotenv()

#security "checks" before the promts are fed to the OPENAI. this is where the pydantic model is used.
class FitnessLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Goal(str, Enum):
    LOSE_WEIGHT = "lose weight"
    GAIN_MUSCLE = "gain muscle"
    GENERAL_FITNESS = "general fitness"
    ENDURANCE = "endurance"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"

class AdviceRequest(BaseModel):
    goal: str = Field(
        ..., 
        description="User's fitness goal",
        example="lose weight"
    )
    fitness_level: str = Field(
        ..., 
        description="User's current fitness level",
        example="beginner"
    )
    question: str = Field(
        ..., 
        description="User's specific question",
        example="What should I eat post workout?",
        min_length=5,
        max_length=500
    )
    

class AdviceResponse(BaseModel):
    advice: str = Field(
        ..., 
        description="AI-generated fitness advice"
    )
    
    #Performance metrics
    moderation_passed: bool = Field(True, description="Whether advice passed safety checks")
    response_time: Optional[float] = Field(None, description="Time taken to generate response (seconds)")
    word_count: Optional[int] = Field(None, description="Number of words in advice")
    

class Config:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
    MAX_TOKENS: int = 300
    TEMPERATURE: float = 0.7
    MODEL: str = "gpt-3.5-turbo" #option b/w this and the gpt-4 model. 
    
    @classmethod
    def validate_api_key(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return True
