#this class is for the bonus content. 
class FitnessModerator:
    HARMFUL_KEYWORDS = [
        "starve", "starvation", "don't eat", "stop eating", "zero calories",
        "no food", "fast for days", "extreme diet",
        
        "steroid", "illegal supplement", "dangerous drug",
        "unprescribed medication",
        
        "ignore pain", "push through injury", "exercise while injured",
        "extreme weight loss", "lose 20 pounds in a week",
        
        "diagnose", "you have", "medical condition", "prescription",
        "medication", "medicine"
    ]
    WARNING_PHRASES = [
        "extreme", "dangerous", "risky", "harmful", "unsafe",
        "medical advice", "see a doctor immediately"
    ]

    #loop to check for harmful advice etc. For the warning phrases, nothing is being done but just a warning is being thrown to take the advice
    #with a grain of salt. 
    @classmethod
    def moderate_advice(cls, advice_text: str) -> dict:
        advice_lower = advice_text.lower()
        warnings = []
        for keyword in cls.HARMFUL_KEYWORDS:
            if keyword in advice_lower:
                return {
                    "passed": False,
                    "reason": f"Contains potentially harmful advice: '{keyword}'",
                    "warnings": warnings
                }
        for phrase in cls.WARNING_PHRASES:
            if phrase in advice_lower:
                warnings.append(f"Contains warning phrase: '{phrase}'")
        
        return {
            "passed": True,
            "reason": None,
            "warnings": warnings
        }
    
    #NPC responses. The actual prompt didn't fail in most of the iterations i tried but just in case. 
    @classmethod
    def get_safe_fallback_advice(cls, goal: str) -> str:
        fallback_advice = {
            "lose weight": "Focus on gradual, sustainable weight loss through a balanced diet and regular exercise. Consult a healthcare professional for personalized advice.",
            "gain muscle": "Build muscle gradually through consistent resistance training and adequate protein intake. Consider working with a certified trainer.",
            "general fitness": "Maintain overall health through regular physical activity, balanced nutrition, and adequate rest. Start slowly and progress gradually."
        }
        
        return fallback_advice.get(
            goal.lower(), 
            "Focus on safe, gradual fitness improvements. Always consult healthcare professionals for personalized advice."
        )
