from flask import Flask, request, render_template, send_file
from googletrans import Translator
from gtts import gTTS
import os
import logging

app = Flask(__name__)

# Define the folder where output files will be saved
OUTPUT_FOLDER = 'static'

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def translate_text(text, target_lang='hi'):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        logging.error(f"Error in translation: {e}")
        return None

def tts_generate(text, lang, filename):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
    except ValueError as e:
        logging.error(f"Error in TTS generation: {e}")
    except Exception as e:
        logging.error(f"Unexpected error in TTS: {e}")

# Route to display the form (GET) or handle form submission (POST)
@app.route('/index', methods=['GET'])
def index():
    # This route renders the input form page
    return render_template('index.html')

# Route to handle the result after form submission
@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        target_lang = request.form.get('target_lang')
        
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
            return f"Unsupported target language. Currently, supported languages are: {', '.join(supported_langs.keys())}."

        # Translate the text
        translated_text = translate_text(input_text, target_lang=target_lang)
        
        if translated_text is None:
            return "Error during translation. Please try again."

        # Ensure the output folder exists, create it if not
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)
        
        # Create the filename based on the target language
        filename = f"{OUTPUT_FOLDER}/{target_lang}_output.wav"
        
        # Delete the old file if it exists
        if os.path.exists(filename):
            os.remove(filename)
        
        # Generate TTS
        try:
            tts_generate(translated_text, lang=target_lang, filename=filename)
        except Exception as e:
            logging.error(f"Error generating TTS: {e}")
            return "Error generating TTS. Please try again."

        # Check if file was created
        if not os.path.exists(filename):
            return "Failed to generate audio file. Please try again."

        # Render the result page with the translated text and generated audio file link
        return render_template('result.html', translated_text=translated_text, filename=filename)

# Route to handle file downloads
@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(f'static/{filename}', as_attachment=True)
    except Exception as e:
        logging.error(f"Error sending file: {e}")
        return "Error downloading file."

if __name__ == '__main__':
    app.run(debug=True)
