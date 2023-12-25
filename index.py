import pyautogui
import time, os
import google.generativeai as genai
from vosk import Model, KaldiRecognizer, SetLogLevel

GOOGLE_API_KEY = "AIzaSyDY78QerX5e30_waM56LSVsVSMIKiOze9U"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

import speech_recognition as sr

def main():
    # Initialisation
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    recognizer.vosk_model = "vosk-model-small-fr-0.22"
    model = Model(model_path=os.path.abspath("vosk-model-fr-0.22"))
    # recognizer.
    # recognizer.set_language("fr-FR")

    # Capture de l'audio
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Conversion de l'audio en texte
    try:
        # transcription = recognizer.recognize_google(audio)
        transcription = recognizer.recognize_vosk(audio)
        print(transcription)
    except sr.UnknownValueError:
        print("La reconnaissance vocale a échoué.")

if __name__ == "__main__":
    main()

# response = model.generate_content("What is the meaning of life?")

# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

# Délai avant le début de l'automatisation (en secondes)
# time.sleep(5)

# # Ouvrir le menu Démarrer
# pyautogui.press('win')
# time.sleep(1)  # Attendre un peu

# # Rechercher et cliquer sur l'application (par exemple, "Notepad")
# pyautogui.write('word')
# time.sleep(1)  # Attendre la recherche
# pyautogui.press('enter')
