import os
import google.generativeai as genai
import sys
import json
import time
from datetime import datetime

# Configure API key
if "GEMINI_API_KEY" not in os.environ:
    print("❌ Error: GEMINI_API_KEY not set. Please export your API key.")
    sys.exit(1)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def ask_gemini(question, retries=3, delay=2):
    """
    Ask Gemini a question with retry logic.
    Retries API call up to `retries` times with `delay` seconds between attempts.
    """
    prompt = f"""
You are a helpful assistant. Answer every question in a clear step-by-step manner.

Important rules:
1. If the question involves science, history, reasoning, or explanations → give a step-by-step explanation.
2. If the question involves math calculation (e.g., addition, subtraction, multiplication, division, algebra) → DO NOT solve it. Instead, politely refuse and suggest using a calculator.

Question: {question}
Answer step-by-step:
    """

    model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-2.0-flash-exp if enabled

    for attempt in range(1, retries + 1):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            if attempt < retries:
                print(f"⏳ Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return f"❌ Failed after {retries} attempts. Error: {e}"

LOG_FILE = 'level1_interaction_log.jsonl'

def log_interaction(question, answer):
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'question': question,
        'answer': answer,
    }
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def main():
    if len(sys.argv) < 2:
        print("Usage: python chatbot.py \"Your question here\"")
        sys.exit(1)

    question = ' '.join(sys.argv[1:])
    answer = ask_gemini(question)

    print("\nAssistant's answer:\n")
    print(answer)

    log_interaction(question, answer)

if __name__ == "__main__":
    main()
