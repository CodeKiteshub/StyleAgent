import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .schemas import (
    ChatRequest,
    ChatResponse,
    AnalyzeRequest,
    AnalyzeResponse,
    RecommendRequest,
    RecommendResponse,
    OutfitRecommendation,
    SocialStats,
    UserContext,
)
from openai import OpenAI
import google.generativeai as genai

load_dotenv()

app = FastAPI(title="StyleAgent Backend", version="0.1.0")

# CORS - adjust origins as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # api_key = os.getenv("OPENAI_API_KEY")
    # if api_key:
    #     try:
    #         client = OpenAI(api_key=api_key)
    #         system_prompt = (
    #             "You are StyleAI, a helpful fashion stylist. "
    #             "Chat naturally and extract the user's context fields: occasion, style_preference, color_preference, budget. "
    #             "Always reply with a short conversational message. "
    #             "Return a JSON object with keys: reply (string) and user_context (object with the four fields; omit unknowns)."
    #         )

    #         messages = [{"role": "system", "content": system_prompt}] + [
    #             {"role": m.role, "content": m.content} for m in req.messages
    #         ]

    #         model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    #         completion = client.chat.completions.create(
    #             model=model,
    #             response_format={"type": "json_object"},
    #             messages=messages,
    #             temperature=0.5,
    #         )

    #         content = completion.choices[0].message.content
    #         data = json.loads(content)

    #         reply = data.get("reply") or "Thanks! Tell me the occasion, style, preferred colors, and budget."
    #         uc = data.get("user_context", {})
    #         user_context = UserContext(
    #             occasion=uc.get("occasion"),
    #             style_preference=uc.get("style_preference"),
    #             color_preference=uc.get("color_preference"),
    #             budget=uc.get("budget"),
    #         )
    #         return ChatResponse(reply=reply, user_context=user_context)
    #     except Exception:
    #         pass

    # Gemini fallback
    gemini_key = os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            model = genai.GenerativeModel(model_name)

            system_prompt = (
                "You are StyleAI, a helpful fashion stylist. "
                "Chat naturally and extract the user's context fields: occasion, style_preference, color_preference, budget. "
                "Always reply with a short conversational message. "
                "Return JSON with keys: reply and user_context."
            )

            # Build conversation history for Gemini
            conversation_text = ""
            for message in req.messages:
                conversation_text += f"{message.role}: {message.content}\n"

            # Gemini JSON guidance
            prompt = (
                system_prompt +
                "\n\nConversation history:\n" + conversation_text +
                "\n\nPlease respond with ONLY valid JSON in this exact format:\n"
                "{\"reply\": \"your conversational response here\", \"user_context\": {\"occasion\": \"value or null\", \"style_preference\": \"value or null\", \"color_preference\": \"value or null\", \"budget\": \"value or null\"}}"
            )

            resp = model.generate_content(prompt)
            text = resp.text.strip() if resp.text else "{}"
            
            # Clean up the response text to extract JSON
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            # Try to find JSON in the response
            start_idx = text.find("{")
            end_idx = text.rfind("}") + 1
            if start_idx != -1 and end_idx > start_idx:
                text = text[start_idx:end_idx]

            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                # If JSON parsing fails, create a basic response
                data = {
                    "reply": "I'm here to help you with your style! Could you tell me about the occasion, your style preference, preferred colors, and budget?",
                    "user_context": {}
                }

            reply = data.get("reply") or "Thanks! Tell me the occasion, style, preferred colors, and budget."
            uc = data.get("user_context", {})
            user_context = UserContext(
                occasion=uc.get("occasion"),
                style_preference=uc.get("style_preference"),
                color_preference=uc.get("color_preference"),
                budget=uc.get("budget"),
            )
            return ChatResponse(reply=reply, user_context=user_context)
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Continue to fallback

    # Fallback behavior (no key or LLM error)
    last_user = next((m for m in reversed(req.messages) if m.role == "user"), None)
    user_context = UserContext()
    if last_user:
        text = last_user.content.lower()
        if "casual" in text:
            user_context.style_preference = "casual"
        if "formal" in text or "professional" in text:
            user_context.style_preference = "professional"
        if "brunch" in text or "party" in text:
            user_context.occasion = "social"

    return ChatResponse(
        reply="Got it! Tell me the occasion, style, preferred colors, and budget.",
        user_context=user_context,
    )


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    # Placeholder analysis
    detected_style = [
        "clean lines",
        "neutral tones",
    ]
    return AnalyzeResponse(
        analysis_summary="Image processed. Detected clean minimalist cues and good posture.",
        detected_body_type=req.user_context.body_type or "average",
        detected_style_cues=detected_style,
    )


def _mock_recommendations() -> list[OutfitRecommendation]:
    return [
        OutfitRecommendation(
            id="1",
            image_url="https://images.pexels.com/photos/1661471/pexels-photo-1661471.jpeg?auto=compress&cs=tinysrgb&w=400",
            title="Chic Minimalist Look",
            caption="Perfect for your casual brunch! Clean lines and neutral tones that complement your style perfectly ✨",
            hashtags=["#minimalist", "#brunch", "#casualchic", "#neutrals", "#effortless"],
            price_range="$150-250",
            body_fit="95% match",
            trend_score=92,
            social_stats=SocialStats(likes=2847, shares=156),
        ),
        OutfitRecommendation(
            id="2",
            image_url="https://images.pexels.com/photos/1926769/pexels-photo-1926769.jpeg?auto=compress&cs=tinysrgb&w=400",
            title="Urban Streetwear Vibe",
            caption="Street style meets comfort - this outfit screams confidence and modern edge 🔥",
            hashtags=["#streetwear", "#urban", "#confident", "#edgy", "#trendy"],
            price_range="$200-350",
            body_fit="88% match",
            trend_score=96,
            social_stats=SocialStats(likes=4231, shares=298),
        ),
        OutfitRecommendation(
            id="3",
            image_url="https://images.pexels.com/photos/1040945/pexels-photo-1040945.jpeg?auto=compress&cs=tinysrgb&w=400",
            title="Classic Professional",
            caption="Timeless elegance for any professional setting. Sharp, sophisticated, and always appropriate 💼",
            hashtags=["#professional", "#classic", "#elegant", "#workwear", "#sophisticated"],
            price_range="$300-450",
            body_fit="90% match",
            trend_score=78,
            social_stats=SocialStats(likes=1689, shares=89),
        ),
        OutfitRecommendation(
            id="4",
            image_url="https://images.pexels.com/photos/1324463/pexels-photo-1324463.jpeg?auto=compress&cs=tinysrgb&w=400",
            title="Casual Weekend Comfort",
            caption="Weekend vibes done right! Comfort meets style in this relaxed yet put-together look 🌟",
            hashtags=["#weekend", "#casual", "#comfortable", "#relaxed", "#effortless"],
            price_range="$100-180",
            body_fit="93% match",
            trend_score=85,
            social_stats=SocialStats(likes=3456, shares=203),
        ),
        OutfitRecommendation(
            id="5",
            image_url="https://images.pexels.com/photos/1139743/pexels-photo-1139743.jpeg?auto=compress&cs=tinysrgb&w=400",
            title="Date Night Ready",
            caption="Dinner date perfection! This look balances sophistication with a hint of playfulness 💕",
            hashtags=["#datenight", "#romantic", "#sophisticated", "#elegant", "#dinner"],
            price_range="$180-280",
            body_fit="91% match",
            trend_score=89,
            social_stats=SocialStats(likes=2934, shares=167),
        ),
        OutfitRecommendation(
            id="6",
            image_url="https://images.pexels.com/photos/1536619/pexels-photo-1536619.jpeg?auto=compress&cs=tinysrgb&w=400",
            title="Bohemian Chic",
            caption="Free-spirited and fabulous! This boho look is perfect for music festivals or artistic events 🌸",
            hashtags=["#boho", "#bohemian", "#artistic", "#freespirit", "#festival"],
            price_range="$120-200",
            body_fit="87% match",
            trend_score=82,
            social_stats=SocialStats(likes=1823, shares=134),
        ),
    ]


@app.post("/api/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    # For now, return the same mock data as the frontend uses
    recs = _mock_recommendations()
    return RecommendResponse(recommendations=recs)


