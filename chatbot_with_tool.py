import os
import sys
import json
import time
from datetime import datetime
import google.generativeai as genai
import calculator_tool  # import your calculator module

# Ensure API key
if "GEMINI_API_KEY" not in os.environ:
    print("❌ Error: GEMINI_API_KEY not set. Please export your API key.")
    sys.exit(1)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

LOG_FILE = "level2_interaction_log.jsonl"


def ask_gemini(question, retries=3, delay=2):
    tool_prompt = f"""
You are a helpful assistant. You have access to a calculator tool.

Rules:
1. If the question involves science, history, reasoning, or explanations → give a step-by-step explanation.
  output format:
  Question: {question}
  Answer step-by-step:
2. If the question involves math (addition, subtraction, multiplication, division) → 
   reply strictly in JSON like this:
   {{
     "action": "use_calculator",
     "expression": "<expression>"
   }}

  or  If the question mixes math with any other request (e.g., "calculate X and also explain Y") → 
   reply strictly in JSON like this:
   {{
     "action": "error",
     "message": "Cannot handle multi-step queries yet. Please ask one thing at a time."
   }}

Important:
- The JSON must be valid and parseable by Python's json.loads.
- Do NOT wrap JSON in markdown code fences.
- For math, always return expressions in symbolic form (e.g., "12+7", "100/5", "(25*4)/2").

Question: {question}
    """
    model = genai.GenerativeModel("gemini-1.5-flash")

    for attempt in range(1, retries + 1):
        try:
            response = model.generate_content(tool_prompt)
            return response.text.strip()
        except Exception as e:
            if attempt < retries:
                print(f"⚠️ Retry {attempt} failed: {e}")
                time.sleep(delay)
            else:
                return json.dumps({"action": "error", "response": str(e)})


def clean_llm_response(raw: str) -> str:
    """
    Strips ```json ... ``` wrappers if Gemini returns them.
    """
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")  # remove backticks
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()
    return raw


def log_interaction(question, answer):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "answer": answer,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    if len(sys.argv) < 2:
        print('Usage: python chatbot_with_tool.py "Your question here"')
        sys.exit(1)

    question = " ".join(sys.argv[1:]).strip()
    raw_response = ask_gemini(question)

    #print(f"\n📥 Raw LLM response:\n{raw_response}\n")

    cleaned = clean_llm_response(raw_response)

    # Try parsing as JSON (only valid if it's math/error case)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        # Not JSON → treat as plain text answer
        answer = cleaned
        print("\n🤖 Assistant's answer:\n")
        print(answer)
        log_interaction(question, answer)
        return

    # Handle JSON responses
    if parsed.get("action") == "use_calculator":
        try:
            expr = parsed["expression"]
            print(f"🧮 Calculator called with expression: {expr}")
            result = calculator_tool.calculate(expr)
            answer = f"The result of your calculation is: {result}"
        except Exception as e:
            answer = f"❌ Calculator failed: {e}"
    elif parsed.get("action") == "error":
        answer = parsed.get("message", "⚠️ An error occurred.")
    else:
        answer = f"⚠️ Unexpected JSON structure: {parsed}"

    print("\n🤖 Assistant's answer:\n")
    print(answer)
    log_interaction(question, answer)


if __name__ == "__main__":
    main()
