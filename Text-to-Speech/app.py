from flask import Flask, request, render_template, send_file
from googletrans import Translator
from gtts import gTTS
from datetime import datetime
import os

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
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
        
        # Generate timestamp for the filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"static/{target_lang}_output_{timestamp}.wav"
        
        # Generate TTS
        tts_generate(translated_text, lang=target_lang, filename=filename)
        
        return render_template('result.html', translated_text=translated_text, filename=filename)
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(f'static/{filename}', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
