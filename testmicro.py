import argparse
import queue
import sys
import sounddevice as sd
# import threading
import json
import os
import google.generativeai as genai
# import pyautogui
import subprocess
import json
import pyttsx4
from gtts import gTTS
from io import BytesIO
from simpleplayer import simpleplayer

from vosk import Model, KaldiRecognizer

engine = pyttsx4.init()
GOOGLE_API_KEY = "AIzaSyDY78QerX5e30_waM56LSVsVSMIKiOze9U"
genai.configure(api_key=GOOGLE_API_KEY)

googlemodel = genai.GenerativeModel('gemini-pro')
preprompt = "Étant donné un texte provenant de l'utilisateur, vous allez interpréter son souhait. Votre tâche consiste a repondre au besoin de l'utilisateur et pour cela vous allez  écrire un json valide ayant une cle 'code' contenant le code Python qui utilise la bibliothèque PyAutoGUI pour exécuter la demande de l'utilisateur sur son ordinateur Windows dans le cas où sa demande implique un action sur l'ordinateur. si sa demande n'implique pas un action sur son ordinateur tu vas donner la reponse dans une cle 'response'. Si vous ne parvenez ou ne pouvez pas à répondre par un action sur l'ordinateur à la demande de l'utilisateur, vous devez renvoyer une clé 'error' contenant vos suggestions ou une reponse appropriée a sa demande. Dans le JSON final, la clé 'code' contiendra le code généré ecris sans utiliser de markdown sachant qu'on peut avoir une erreur. voici la demande de l'utilisateur : "


q = queue.Queue()

def execute_code(code):
    # Écriture du code Python dans un fichier
        with open("action.py", "w") as f:
            f.write(code)

        # Exécution du code Python
        # pyautogui.run
        # pyautogui.run_script("action.py")
        subprocess.run(['python', 'action.py'])

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def start_listening():
    print('ok cool')

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "-l", "--list-devices", action="store_true",
        help="show list of audio devices and exit")
    parser.add_argument(
        "-f", "--filename", type=str, metavar="FILENAME",
        help="audio file to store recording to")
    parser.add_argument(
        "-d", "--device", type=int_or_str,
        help="input device (numeric ID or substring)")
    parser.add_argument(
        "-r", "--samplerate", type=int, help="sampling rate")
    parser.add_argument(
        "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
    args = parser.parse_args()

    try:
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, "input")
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info["default_samplerate"])

        if args.model is None:
            model = Model(model_path=os.path.abspath("vosk-model-fr-0.22"))
        else:
            model = Model(lang=args.model)

        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None
        rec = KaldiRecognizer(model, args.samplerate)

        with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device,
                               dtype="int16", channels=1, callback=callback):
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    print(result)
                    result = json.loads(result)
                    # Process the recognized text here (e.g., print it, save it, etc.)
                    # Replace this line with your desired code to handle the recognized text
                    print(result['text'])
                    if(len(result['text'])>0):
                        response = googlemodel.generate_content(preprompt+result["text"])
                        print(response.text[7:-3].strip())
                        with open('data.json', 'w') as f:
                            # contenu = f.read()
                            f.write(response.text[7:-3].strip())
                        
                        
                        with open("data.json", "r") as f:
                            text = f.read()
                            try:
                                text = json.loads(text)
                                if 'code' in text:
                                    print(text["code"])
                                    execute_code(text["code"])
                                else:
                                    if 'response' in text:
                                        print(text["response"])
                                        tts = gTTS(text['response'], lang='fr')
                                        tts.save("mp3.mp3")
                                        player = simpleplayer('mp3.mp3')
                                        player.play()
                                    else:
                                        print(text["error"])
                                        
                                        tts = gTTS(text['error'], lang='fr')
                                        tts.save("mp3.mp3")
                                        player = simpleplayer('mp3.mp3')
                                        player.play()
                            except:
                                pass
                        
                else:
                    pass

                if dump_fn is not None:
                    dump_fn.write(data)

    except KeyboardInterrupt:
        print("\nDone")
    except Exception as e:
        print(type(e).__name__ + ": " + str(e))

if __name__ == "__main__":
    start_listening()