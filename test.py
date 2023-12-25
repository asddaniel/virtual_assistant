import json, subprocess

# text = '{"code": "import pyautogui\\n\\npyautogui.press(\'win\')\\npyautogui.write(\'Explorateur de fichiers\')\\npyautogui.press(\'enter\')"}'
# data = json.loads(text)
# print(data["code"])



# def execute_code(code):
#     # Écriture du code Python dans un fichier
#         with open("action.py", "w") as f:
#             f.write(code)

#         # Exécution du code Python
#         # pyautogui.run
#         # pyautogui.run_script("action.py")
#         subprocess.run(['python', 'action.py'])

# with open("data.json", "r") as f:
#       text = f.read()
#       text = json.loads(text)
#       print(text["code"])
#       execute_code(text["code"])

from gtts import gTTS
from io import BytesIO

mp3_fp = BytesIO()
tts = gTTS('Bonjour Monsieur', lang='fr')
tts.save("mp3.mp3")

from simpleplayer import simpleplayer

player = simpleplayer('mp3.mp3')
player.play()
