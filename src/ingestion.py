import json
import re

def clean_and_parse_json(text):
    """
    Cleans dirty JSON (comments, trailing commas) and parses it.
    """
    # 1. Remove comments (// ...)
    text = re.sub(r'(?<!:)//.*', '', text)
    
    # 2. Remove trailing commas before closing braces/brackets
    # Matches a comma, optional whitespace, then } or ]
    text = re.sub(r',\s*([\]}])', r'\1', text)
    
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        # Fallback: Try identifying simple errors
        return {"error": f"Failed to parse JSON even after cleaning. Details: {str(e)}"}

def load_json(uploaded_file):
    if uploaded_file is not None:
        try:
            # Read file as string
            content = uploaded_file.getvalue().decode("utf-8")
            return clean_and_parse_json(content)
        except Exception as e:
            return {"error": f"File Read Error: {str(e)}"}
    return None

def extract_audit_data(chat_json, context_json):
    """
    Intelligently extracts the last user query, AI response, and context.
    """
    try:
        # Propagate errors if previous steps failed
        if isinstance(chat_json, dict) and "error" in chat_json: return chat_json
        if isinstance(context_json, dict) and "error" in context_json: return context_json

        # 1. Parse Chat Log
        turns = chat_json.get('conversation_turns', [])
        user_msg = "Unknown"
        ai_msg = "Unknown"
        
        # Reverse search for the last AI response
        for i in range(len(turns)-1, 0, -1):
            if turns[i]['role'] == 'AI/Chatbot':
                ai_msg = turns[i]['message']
                # The turn before AI should be the User
                if turns[i-1]['role'] == 'User':
                    user_msg = turns[i-1]['message']
                break

        # 2. Parse Context (Ground Truth)
        vectors = context_json.get('data', {}).get('vector_data', [])
        context_text = ""
        for idx, item in enumerate(vectors):
            text = item.get('text', '').strip()
            context_text += f"[Source {idx+1}]: {text}\n\n"

        return {
            "query": user_msg,
            "response": ai_msg,
            "context": context_text
        }
    except Exception as e:
        return {"error": f"Extraction Error: {str(e)}"}