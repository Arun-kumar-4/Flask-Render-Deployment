# # import pyttsx3
# # from pydub import AudioSegment
# # import os

# # def text_to_mp3(text, filename):
# #     engine = pyttsx3.init()
    
# #     temp_wav = "temp.wav"
# #     engine.save_to_file(text, temp_wav)
# #     engine.runAndWait()

# # if __name__ == "__main__":
# #     text = input("Enter the text to translate (in English): ")
# #     filename = "result.mp3"
# #     text_to_mp3(text, filename)


# from google.cloud import texttospeech
# from datetime import datetime

# def tts_generate_google(text, lang, filename):
#     client = texttospeech.TextToSpeechClient()

#     synthesis_input = texttospeech.SynthesisInput(text=text)
#     voice = texttospeech.VoiceSelectionParams(
#         language_code=lang,
#         ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
#     )
#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.LINEAR16
#     )

#     response = client.synthesize_speech(
#         input=synthesis_input,
#         voice=voice,
#         audio_config=audio_config
#     )

#     with open(filename, 'wb') as out:
#         out.write(response.audio_content)
#         print(f"TTS audio saved as {filename}")

# # User input
# input_text = input("Enter the text to translate (in English): ")
# target_lang = 'or-IN'  # Language code for Odia in Google Cloud TTS

# # Generate timestamp for the filename
# timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
# filename = f"{target_lang}_output_{timestamp}.wav"

# # Generate TTS
# tts_generate_google(input_text, lang=target_lang, filename=filename)


from google.cloud import texttospeech
from datetime import datetime

def tts_generate_google(text, lang, filename):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(filename, 'wb') as out:
        out.write(response.audio_content)
        print(f"TTS audio saved as {filename}")

# User input
input_text = input("Enter the text to translate (in English): ")
target_lang = 'or-IN'  # Language code for Odia in Google Cloud TTS

# Generate timestamp for the filename
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f"{target_lang}_output_{timestamp}.wav"

# Generate TTS
tts_generate_google(input_text, lang=target_lang, filename=filename)
