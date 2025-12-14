from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse  # Import for redirection
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv

# Import Logic
from src.ingestion import extract_audit_data
from src.metrics import calculate_tech_metrics
from src.judge import evaluate_relevance, evaluate_faithfulness

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Frontend Files
app.mount("/app", StaticFiles(directory="static", html=True), name="static")

@app.post("/analyze")
async def analyze_audit(
    chat_file: UploadFile = File(...), 
    context_file: UploadFile = File(...)
):
    try:
        # READ FILES
        chat_bytes = await chat_file.read()
        context_bytes = await context_file.read()
        
        import re
        def parse_raw(text_bytes):
            text = text_bytes.decode("utf-8")
            text = re.sub(r'(?<!:)//.*', '', text) 
            text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
            text = re.sub(r',(\s*[}\]])', r'\1', text)
            return json.loads(text)

        chat_json = parse_raw(chat_bytes)
        context_json = parse_raw(context_bytes)

        # EXTRACT DATA
        turns = chat_json.get('conversation_turns', [])
        user_msg = "Unknown"
        ai_msg = "Unknown"
        
        for i in range(len(turns)-1, 0, -1):
            if turns[i].get('role') == 'AI/Chatbot':
                ai_msg = turns[i].get('message', '')
                if i > 0: user_msg = turns[i-1].get('message', '')
                break
        
        vectors = context_json.get('data', {}).get('vector_data', [])
        context_text = "\n".join([f"[Source {i}]: {v.get('text','')}" for i, v in enumerate(vectors)])

        # RUN AI LOGIC
        tech = calculate_tech_metrics(user_msg, context_text, ai_msg)
        rel_score, rel_reason = evaluate_relevance(user_msg, ai_msg)
        faith_score, faith_reason = evaluate_faithfulness(ai_msg, context_text)

        return {
            "status": "success",
            "query": user_msg,
            "response": ai_msg,
            "metrics": tech,
            "scores": {
                "relevance": {"score": rel_score, "reason": rel_reason},
                "faithfulness": {"score": faith_score, "reason": faith_reason}
            }
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- ROOT REDIRECT (This solves the 404 error) ---
@app.get("/")
async def root():
    return RedirectResponse(url="/app/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)