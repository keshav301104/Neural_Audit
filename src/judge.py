import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

def get_llm():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API Key not found")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # You can keep 2.5 if it works for you
        temperature=0,
        google_api_key=api_key
    )

def clean_and_split(text):
    """
    Safely splits the AI output into [Score, Reason].
    Handles cases where AI is too chatty or format is wrong.
    """
    # Force limit to 1 split (max 2 items)
    parts = text.split("|", 1)
    
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    elif len(parts) == 1:
        # If AI forgot the pipe, assume the whole text is the reason
        return 0, parts[0].strip()
    else:
        return 0, "Error parsing AI response"

def evaluate_relevance(query, response):
    try:
        llm = get_llm()
        prompt = ChatPromptTemplate.from_template("""
        You are a strict Logic Auditor.
        USER QUERY: {q}
        AI RESPONSE: {r}
        Did the AI directly answer the specific question asked?
        - If yes and complete: 100
        - If yes but missing details: 75
        - If vague: 50
        - If irrelevant: 0
        
        Output ONLY: Score|Reason
        Example: 80|Answered core question but missed details.
        """)
        res = llm.invoke(prompt.format(q=query, r=response))
        
        # USE THE SAFE SPLITTER
        return clean_and_split(res.content)
        
    except Exception as e:
        return 0, f"System Error: {str(e)}"

def evaluate_faithfulness(response, context):
    try:
        llm = get_llm()
        prompt = ChatPromptTemplate.from_template("""
        You are a Fact-Checking Auditor.
        GROUND TRUTH: {c}
        AI CLAIM: {r}
        Does the AI Claim contain ANY information NOT found in the Ground Truth?
        - If PERFECTLY supported: 100
        - If minor additions: 50
        - If Hallucination: 0
        
        Output ONLY: Score|Reason
        Example: 0|Mentioned facts not in source.
        """)
        res = llm.invoke(prompt.format(c=context, r=response))
        
        # USE THE SAFE SPLITTER
        return clean_and_split(res.content)
        
    except Exception as e:
        return 0, f"System Error: {str(e)}"