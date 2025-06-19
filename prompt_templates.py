from typing import Dict, Any

class FitnessPromptTemplates:
    BASE_PERSONA = """You are a certified personal trainer and nutrition coach with 10 years of experience. 
You provide safe, practical, and evidence-based fitness advice. You always prioritize safety and remind users 
to consult healthcare professionals for medical concerns or injuries. Your advice is encouraging but realistic. You will not provide extreme or harmful advice. Do not
be redundant. Stay to the point"""

    SAFETY_DISCLAIMER = """
Important: This advice is for educational purposes only and doesn't replace professional medical advice. 
Always consult with a healthcare provider before starting any new exercise program, especially if you have 
health conditions or injuries."""

    @staticmethod
    def _format_user_profile(goal: str, fitness_level: str) -> str:
        return f"""User Profile:
- Goal: {goal}
- Fitness Level: {fitness_level}"""

    @staticmethod
    def _format_base_structure(persona_or_context: str, goal: str, fitness_level: str, question: str, instruction: str) -> str:
        return f"""{persona_or_context}

{FitnessPromptTemplates._format_user_profile(goal, fitness_level)}

User Question: {question}

{instruction}{FitnessPromptTemplates.SAFETY_DISCLAIMER}"""

    @classmethod
    def get_basic_prompt(cls, goal: str, fitness_level: str, question: str) -> str:
        instruction = "Please provide helpful, safe advice tailored to their goal and fitness level. Keep your response clear and actionable."
        return cls._format_base_structure(cls.BASE_PERSONA, goal, fitness_level, question, instruction)

    @classmethod
    def get_goal_specific_prompt(cls, goal: str, fitness_level: str, question: str) -> str:

        goal_contexts = {
            "lose weight": "Focus on sustainable weight loss through proper nutrition and exercise. Emphasize caloric deficit and healthy food.",
            "gain muscle": "Focus on muscle building through resistance training and proper nutrition. Emphasize adequate protein and recovery period.",
            "general fitness": "Focus on overall health and wellness. Emphasize balanced approach to cardio, strength, and flexibility.",
            "endurance": "Focus on cardiovascular fitness and stamina. Emphasize aerobic and endurance training.",
            "strength": "Focus on maximal strength development. Emphasize compound movements, progressive overload, and proper form.",
            "flexibility": "Focus on mobility and flexibility. Emphasize stretching and injury prevention."
        }
        
        goal_context = goal_contexts.get(goal.lower(), "Focus on safe, effective fitness practices.")
        persona_with_context = f"{cls.BASE_PERSONA}\n\nSpecialization Context: {goal_context}"
        instruction = "Provide specific advice that aligns with their goal. Adjust the complexity of your explanation based on their fitness level."
        
        return cls._format_base_structure(persona_with_context, goal, fitness_level, question, instruction)

    @classmethod
    def get_level_adapted_prompt(cls, goal: str, fitness_level: str, question: str) -> str:
        level_instructions = {
            "beginner": "Use simple, clear language. Explain basic concepts. Focus on form and safety. Provide step-by-step instructions.",
            "intermediate": "Use moderate technical language. Assume basic knowledge of exercises. Provide some advanced tips.",
            "advanced": "Use technical fitness terminology. Assume extensive knowledge. Focus on optimization and advanced techniques."
        }
        
        level_instruction = level_instructions.get(fitness_level.lower(), "Adjust your language appropriately.")
        persona_with_context = f"{cls.BASE_PERSONA}\n\nCommunication Style: {level_instruction}"
        instruction = "Tailor your response complexity to match their fitness level while providing valuable, actionable advice."
        
        return cls._format_base_structure(persona_with_context, goal, fitness_level, question, instruction)

class PromptSelector:
    @staticmethod
    def select_prompt_strategy(goal: str, fitness_level: str, question: str) -> str:
        return FitnessPromptTemplates.get_goal_specific_prompt(goal, fitness_level, question)
    
    #this was done during the dev stage to compare all ther prompt responses. 
    @staticmethod
    def get_all_prompt_versions(goal: str, fitness_level: str, question: str) -> Dict[str, str]:
        return {
            "basic": FitnessPromptTemplates.get_basic_prompt(goal, fitness_level, question),
            "goal_specific": FitnessPromptTemplates.get_goal_specific_prompt(goal, fitness_level, question),
            "level_adapted": FitnessPromptTemplates.get_level_adapted_prompt(goal, fitness_level, question)
        }

