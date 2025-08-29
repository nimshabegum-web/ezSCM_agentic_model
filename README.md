# Gemini Smart Assistant: Multi-Level CLI Bots

This project demonstrates three levels of a smart assistant using Google Gemini LLM, calculator, and translation tools. Each level adds more capabilities and complexity.

---

## Table of Contents

- [Features by Level](#features-by-level)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
  - [Level 1: LLM-Only Chatbot](#level-1-llm-only-chatbot)
  - [Level 2: Chatbot with Calculator Tool](#level-2-chatbot-with-calculator-tool)
  - [Level 3: Full Agent (Multi-Tool, Multi-Step)](#level-3-full-agent-multi-tool-multi-step)
- [Logs](#logs)
- [File Structure](#file-structure)
- [Notes](#notes)
- [Example Interactions](#example-interactions)

---

## Features by Level

- **Level 1 (`chatbot.py`):**  
  - Answers questions with step-by-step explanations.
  - Refuses to solve math directly; suggests using a calculator.
  - Logs all interactions.

- **Level 2 (`chatbot_with_tool.py`):**  
  - Uses Gemini LLM and a calculator tool.
  - Handles single-step math queries via calculator.
  - Refuses multi-step queries (e.g., "calculate X and explain Y").
  - Logs all interactions.

- **Level 3 (`full_agent.py`):**  
  - Handles multi-step queries.
  - Can use calculator and translator tools, or answer directly.
  - Breaks down complex queries into ordered steps and executes them.
  - Logs all plans and results.

---

## Setup & Installation

1. **Clone the repository** (if not already done):

   ```sh
   git clone https://github.com/nimshabegum-web/ezSCM_agentic_model.git
   cd ezSCM_agentic_model
   ```

2. **Create and activate a Python virtual environment:**

   - **Windows (Command Prompt):**
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux/macOS:**
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Python dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Get a Gemini API key:**

   - Sign up and obtain an API key from [Google AI developers console](https://ai.google.com/).
   -after sign up create API key from https://aistudio.google.com/app/apikey

5. **Set the Gemini API key as an environment variable:**

   - **Linux/macOS (bash/zsh):**
     ```sh
     export GEMINI_API_KEY="your_api_key_here"
     ```
   - **Windows Command Prompt:**
     ```cmd
     set GEMINI_API_KEY=your_api_key_here
     ```
   - **Windows PowerShell:**
     ```powershell
     $env:GEMINI_API_KEY="your_api_key_here"
     ```

---

## Usage

### Level 1: LLM-Only Chatbot

- **Run:**
  ```sh
  python chatbot.py "What are the colors in a rainbow?"
  ```

- **Behavior:**  
  Answers with step-by-step explanations. Refuses to solve math directly.

- **Log file:**  
  [`level1_interaction_log.jsonl`](level1_interaction_log.jsonl)

---

### Level 2: Chatbot with Calculator Tool

- **Run:**
  ```sh
  python chatbot_with_tool.py "What is 12 times 7?"
  ```

- **Behavior:**  
  - Uses Gemini to decide if the question is math or not.
  - For math, calls the calculator tool and returns the result.
  - For non-math, gives explanations.
  - Refuses multi-step queries.

- **Log file:**  
  [`level2_interaction_log.jsonl`](level2_interaction_log.jsonl)

---

### Level 3: Full Agent (Multi-Tool, Multi-Step)

- **Run:**
  ```sh
  python full_agent.py "Translate 'Good Morning' into German and then multiply 5 and 6."
  ```

- **Behavior:**  
  - Breaks down complex queries into steps (calculator, translator, direct answer).
  - Executes each step and prints/logs results.

- **Log file:**  
  [`level3_interaction_log.jsonl`](level3_interaction_log.jsonl)

---

## Logs

Each level writes logs in JSON Lines format, including timestamps, questions, and answers (or plans/results for Level 3):

- Level 1: [`level1_interaction_log.jsonl`](level1_interaction_log.jsonl)
- Level 2: [`level2_interaction_log.jsonl`](level2_interaction_log.jsonl)
- Level 3: [`level3_interaction_log.jsonl`](level3_interaction_log.jsonl)

---

## File Structure

- [`chatbot.py`](chatbot.py) — Level 1: LLM-only chatbot.
- [`chatbot_with_tool.py`](chatbot_with_tool.py) — Level 2: Chatbot with calculator tool.
- [`full_agent.py`](full_agent.py) — Level 3: Full agent with calculator and translator tools.
- [`calculator_tool.py`](calculator_tool.py) — Calculator utility.
- [`translator_tool.py`](translator_tool.py) — English→German translation utility.
- `level1_interaction_log.jsonl`, `level2_interaction_log.jsonl`, `level3_interaction_log.jsonl` — Log files.
- [`README.md`](README.md) — This documentation.

---

## Notes

- All scripts require the `GEMINI_API_KEY` environment variable.
- For translation, Level 3 uses the `deep-translator` package.
- Calculator tool only supports simple binary operations (+, -, *, /).
- Each script is independent; run the one matching your desired level.

---

## Example Interactions

**Level 1:**
```sh
python chatbot.py "What are the colors in a rainbow?"
```
*Assistant's answer:*
```
Step 1:  A rainbow displays a spectrum of colors, not just a set number.
Step 2: However, a commonly used mnemonic helps remember the main colors. This mnemonic is ROY G. BIV.
...
```

**Level 2:**
```sh
python chatbot_with_tool.py "What is 12 times 7?"
```
*Assistant's answer:*
```
The result of your calculation is: 84.0
```

**Level 3:**
```sh
python full_agent.py "Translate 'Good Morning' into German and then multiply 5 and 6."
```
*Final Answer:*
```
Translation: 'Good Morning' → 'Guten Morgen'
Calculator result: 5*6 = 30.0
```

---

For any issues, please check your API key, dependencies, and refer to the log files for
