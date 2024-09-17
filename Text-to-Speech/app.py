from flask import Flask, request, render_template, send_file
from googletrans import Translator
from gtts import gTTS
import os

app = Flask(__name__)

# Define the folder where output files will be saved
OUTPUT_FOLDER = 'static'

def translate_text(text, target_lang='hi'):
    translator = Translator()
    translation = translator.translate(text, dest=target_lang)
    return translation.text

def tts_generate(text, lang, filename):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
    except ValueError as e:
        print(f"Error in TTS generation: {e}")

# Route to display the form (GET) or handle form submission (POST)
@app.route('/index', methods=['GET'])
def index():
    # This route renders the input form page
    return render_template('index.html')

# Route to handle the result after form submission
@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        input_text = request.form['input_text']
        target_lang = request.form['target_lang']
        
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
        
        # Ensure the output folder exists, create it if not
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)
        
        # Create the filename based on the target language
        filename = f"{OUTPUT_FOLDER}/{target_lang}_output.wav"
        
        # Delete the old file if it exists
        if os.path.exists(filename):
            os.remove(filename)
        
        # Generate TTS
        tts_generate(translated_text, lang=target_lang, filename=filename)
        
        # Render the result page with the translated text and generated audio file link
        return render_template('result.html', translated_text=translated_text, filename=filename)

# Route to handle file downloads
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(f'static/{filename}', as_attachment=True)

if __name__ == '__main__':
    app.run()
