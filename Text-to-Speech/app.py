from flask import Flask, request, render_template, send_file, redirect, url_for
from googletrans import Translator
from gtts import gTTS
import io
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Dictionary to store audio for each session
audio_storage = {}

def translate_text(text, target_lang='hi'):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        logging.error(f"Error in translation: {e}")
        return None

def tts_generate_in_memory(text, lang):
    try:
        tts = gTTS(text=text, lang=lang)
        audio_file = io.BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        return audio_file
    except ValueError as e:
        logging.error(f"Error in TTS generation: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in TTS: {e}")
        return None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

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

        # Generate TTS audio in memory
        audio_file = tts_generate_in_memory(translated_text, lang=target_lang)
        
        if audio_file is None:
            return "Error generating TTS. Please try again."

        # Store the audio file in the dictionary
        session_id = request.cookies.get('session_id', 'default')
        audio_storage[session_id] = audio_file

        # Render result page with a link to listen to the audio or download it
        return render_template('result.html', translated_text=translated_text, session_id=session_id)

@app.route('/play')
def play_audio():
    session_id = request.args.get('session_id', 'default')
    audio_file = audio_storage.get(session_id)
    
    if audio_file is None:
        return "Audio not available. Please generate it first."
    
    return send_file(audio_file, mimetype='audio/wav', as_attachment=False)

@app.route('/download')
def download_audio():
    session_id = request.args.get('session_id', 'default')
    audio_file = audio_storage.get(session_id)
    
    if audio_file is None:
        return "Audio not available. Please generate it first."
    
    return send_file(audio_file, mimetype='audio/wav', as_attachment=True, download_name='output.wav')

if __name__ == '__main__':
    app.run(debug=True)
