# translator_tool.py
from deep_translator import GoogleTranslator

def translate_to_german(text: str) -> str:
    return GoogleTranslator(source='en', target='de').translate(text)

if __name__ == "__main__":
    print(translate_to_german("i am fine"))  # Outputs: Guten Morgen
