from datetime import datetime, timezone
import json
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from app.core.logger import logger

SYSTEM_PROMPT = """
You are "Adhi Blood Connect AI", a specialized medical assistant dedicated exclusively to blood donation safety, FAQs, eligibility requirements, compatibility guidance, and post-donation care tips.

Strict guidelines you must follow:
1. Provide accurate, clear, and reassuring guidance about blood donation.
2. If the user asks about blood compatibility, refer to standard donor-recipient matrices.
3. Explicitly state that you are an AI assistant, and your advice is for informational purposes only and does not replace professional medical consultations.
4. Politely decline answering questions that are completely unrelated to medicine, health, or blood donation.
5. Do not offer complex medical diagnoses. If symptoms are critical, urge the user to visit an emergency room immediately.
"""

class ChatbotService:
    """
    AI integration service communicating with Gemini or OpenAI. Logs conversational analytics in MongoDB.
    """
    @staticmethod
    async def ask_chatbot(db: AsyncIOMotorDatabase, message: str, user_id: str = "anonymous") -> dict:
        """
        Sends query to the configured AI API (Gemini or OpenAI) with context-tuning prompts.
        Logs the transaction to the 'chatbot_logs' collection.
        """
        prompt = message.strip()
        logger.info(f"AI Chatbot inquiry received from User ID '{user_id}': '{prompt[:30]}...'")
        
        reply = ""
        model_used = "fallback-rule-engine"
        
        # 1. Try Gemini API if key is available
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
                response = model.generate_content(prompt)
                reply = response.text
                model_used = "gemini-1.5-flash"
                logger.info("Successfully fetched response from Gemini API.")
            except Exception as e:
                logger.error(f"Gemini API execution failed: {str(e)}")

        # 2. Try OpenAI API if Gemini failed or is not configured
        if not reply and settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
                completion = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=400
                )
                reply = completion.choices[0].message.content
                model_used = "gpt-4o-mini"
                logger.info("Successfully fetched response from OpenAI API.")
            except Exception as e:
                logger.error(f"OpenAI API execution failed: {str(e)}")

        # 3. Fallback rule engine (if keys are missing or API limits are hit)
        if not reply:
            reply = ChatbotService._rule_based_fallback(prompt)
            logger.info("Executed smart rule-based fallback response.")

        # Log conversation to MongoDB
        log_doc = {
            "user_id": user_id,
            "query": prompt,
            "reply": reply,
            "model": model_used,
            "created_at": datetime.now(timezone.utc)
        }
        try:
            await db["chatbot_logs"].insert_one(log_doc)
        except Exception as e:
            logger.error(f"Failed to write chat log to MongoDB: {str(e)}")

        # Provide helpful suggestions for frontend buttons
        suggestions = ChatbotService._generate_suggestions(prompt)
        
        return {
            "reply": reply,
            "suggestions": suggestions
        }

    @staticmethod
    def _rule_based_fallback(query: str) -> str:
        """
        Provides accurate medical guidelines for blood donation in case APIs are not configured.
        """
        q = query.lower()
        
        # General FAQ Matchers
        if "compatible" in q or "blood group" in q or "receive" in q or "give" in q:
            return (
                "Regarding blood compatibility, here is a quick guide:\n"
                "- **O negative (O-)** is the universal donor; O- red blood cells can be given to anyone.\n"
                "- **AB positive (AB+)** is the universal recipient; they can receive any type of red blood cells.\n"
                "- Generally, positive blood types can receive positive or negative blood, but negative types can only receive negative blood.\n\n"
                "Please consult a physician for clinical questions. I'm here to help you register or match donors!"
            )
        elif "eligible" in q or "requirement" in q or "who can" in q:
            return (
                "General requirements to donate blood include:\n"
                "- **Age**: Usually between 18 to 65 years old.\n"
                "- **Weight**: Minimum of 50 kg (110 lbs).\n"
                "- **Health**: You must feel healthy, and be free of active infections, colds, or flu.\n"
                "- **Donation Interval**: At least 90 days must have passed since your last whole blood donation.\n\n"
                "Before donating, your vitals (hemoglobin levels, blood pressure, temperature) will always be evaluated at the donation center."
            )
        elif "care" in q or "after" in q or "post" in q or "dizzy" in q:
            return (
                "After donating blood, we recommend following these post-donation care tips:\n"
                "1. Keep the bandage on your arm for at least 4-5 hours.\n"
                "2. Drink plenty of extra fluids (water, juices) for the next 24-48 hours.\n"
                "3. Avoid strenuous physical activity or lifting heavy weights for the rest of the day.\n"
                "4. If you feel lightheaded, sit down or lie down with your legs elevated until it passes.\n"
                "5. Eat iron-rich foods to help rebuild your red blood cells.\n\n"
                "If bleeding persists or you feel severely unwell, contact a doctor immediately."
            )
        else:
            return (
                "Welcome to Adhi Blood Connect! I can help you with queries regarding blood donation requirements, compatibility, "
                "post-donation tips, and emergency blood requests.\n\n"
                "For your safety, please note that I am an AI assistant; my suggestions are for informational purposes only. "
                "How can I assist you with blood donation today?"
            )

    @staticmethod
    def _generate_suggestions(query: str) -> list:
        """
        Suggests relevant follow-up questions to display as quick buttons.
        """
        q = query.lower()
        if "compatible" in q or "blood group" in q:
            return ["Am I eligible to donate?", "What are post-donation tips?", "How do I create emergency requests?"]
        elif "eligible" in q or "requirement" in q:
            return ["Tell me about blood compatibility", "How often can I donate?", "Post-donation care guidelines"]
        return ["Who is eligible to donate?", "Tell me about blood compatibility", "Post-donation care tips"]
