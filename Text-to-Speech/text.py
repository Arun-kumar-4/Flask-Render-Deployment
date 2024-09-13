from googletrans import Translator
from gtts import gTTS
from datetime import datetime

def translate_text(text, target_lang='hi'):
    translator = Translator()
    translation = translator.translate(text, dest=target_lang)
    return translation.text

def tts_generate(text, lang, filename):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        print(f"TTS audio saved as {filename}")
    except ValueError as e:
        print(f"Error in TTS generation: {e}")

# User input
input_text = input("Enter the text to translate (in English): ")
target_lang = input("Enter the target language (e.g., 'hi' for Hindi, 'ta' for Tamil, 'bn' for Bengali, 'mr' for Marathi, 'or' for Odia, 'gu' for Gujarati, 'te' for Telugu, 'en' for English): ").strip().lower()

# Validate language input
supported_langs = {
    'hi': 'Hindi',
    'ta': 'Tamil',
    'bn': 'Bengali',
    'mr': 'Marathi',
    'or': 'Odia',
    'gu': 'Gujarati',
    'te': 'Telugu',
    'en': 'English'
}

if target_lang not in supported_langs:
    print(f"Unsupported target language. Currently, supported languages are: {', '.join(supported_langs.keys())}.")
else:
    # Translate the text
    translated_text = translate_text(input_text, target_lang=target_lang)
    print("Translated Text:", translated_text)

    # Generate timestamp for the filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{target_lang}_output_{timestamp}.wav"
    
    # Generate TTS
    tts_generate(translated_text, lang=target_lang, filename=filename)
