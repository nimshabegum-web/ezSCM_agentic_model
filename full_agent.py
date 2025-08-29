# full_agent.py
import os
import sys
import json
import time
from datetime import datetime
import google.generativeai as genai
import calculator_tool
import translator_tool

# Ensure API key
if "GEMINI_API_KEY" not in os.environ:
    print("❌ Error: GEMINI_API_KEY not set. Please export your API key.")
    sys.exit(1)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

LOG_FILE = "level3_interaction_log.jsonl"


def ask_gemini(question, retries=3, delay=2):
    """
    Calls Gemini to break down multi-step queries into structured JSON plan.
    """
    tool_prompt = f"""
You are a helpful assistant. You have access to:
- calculator_tool (for +, -, *, /)
- translator_tool (English → German)
- your own knowledge (for reasoning, history, science answers).

Rules:
1. Break the user query into ordered steps.
2. For each step, decide one of:
   - "use_calculator" with an expression
   - "use_translator" with a phrase
   - "answer_direct" with a reasoning/explanation
3. Return the entire plan in valid JSON.
4. Do NOT wrap in code fences.

Example:
User: "Translate 'Good Morning' into German and then multiply 5 and 6."
Output:
{{
  "steps": [
    {{"action": "use_translator", "text": "Good Morning"}},
    {{"action": "use_calculator", "expression": "5*6"}}
  ]
}}

User: "What is the capital of Italy, then multiply 12 and 12."
Output:
{{
  "steps": [
    {{"action": "answer_direct", "response": "The capital of Italy is Rome."}},
    {{"action": "use_calculator", "expression": "12*12"}}
  ]
}}

Now process this question strictly in the same JSON structure:

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
                return json.dumps({"steps": [{"action": "error", "message": str(e)}]})


def clean_llm_response(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()
    return raw


def log_interaction(question, steps, results):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "plan": steps,
        "results": results,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def execute_steps(steps):
    results = []
    for i, step in enumerate(steps, 1):
        action = step.get("action")
        print(f"\n➡️ Step {i}: {step}")
        try:
            if action == "use_calculator":
                expr = step["expression"]
                result = calculator_tool.calculate(expr)
                results.append(f"Calculator result: {expr} = {result}")
            elif action == "use_translator":
                text = step["text"]
                result = translator_tool.translate_to_german(text)
                results.append(f"Translation: '{text}' → '{result}'")
            elif action == "answer_direct":
                result = step["response"]
                results.append(f"Answer: {result}")
            else:
                result = f"⚠️ Unknown action: {action}"
                results.append(result)
        except Exception as e:
            results.append(f"❌ Error executing step: {e}")
    return results


def main():
    if len(sys.argv) < 2:
        print('Usage: python full_agent.py "Your question here"')
        sys.exit(1)

    question = " ".join(sys.argv[1:]).strip()
    raw_response = ask_gemini(question)
    cleaned = clean_llm_response(raw_response)

    try:
        parsed = json.loads(cleaned)
        steps = parsed.get("steps", [])
    except json.JSONDecodeError:
        print(f"⚠️ Invalid JSON from LLM: {cleaned}")
        return

    results = execute_steps(steps)

    print("\n🤖 Final Answer:\n")
    for r in results:
        print(r)

    log_interaction(question, steps, results)


if __name__ == "__main__":
    main()
