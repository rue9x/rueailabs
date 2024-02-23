#import library
import keyboard
import speech_recognition as sr
from openai import OpenAI
from elevenlabs import generate, play, Voice, VoiceSettings
import base64
import json
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6 import QtGui
import sys
import time
with open('config.json','r') as fi:
    config = json.load(fi)

with open('voices.json','r') as fi:
    voices = json.load(fi)

voice = voices[config['voice']]

config["open_ai_key"] = base64.b64decode(config["open_ai_key"]).decode('utf-8')
config["elevenlabs_key"] = base64.b64decode(config["elevenlabs_key"]).decode('utf-8')
config["azure_key"] = base64.b64decode(config["azure_key"]).decode('utf-8') # not supported yet
key = "f12"
quit_key = "esc"
convo_history = ""

#open ai setup
client = OpenAI(api_key=config["open_ai_key"])

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

 # Reading Microphone as source
# listening the speech and store in audio_text variable
voice =Voice(
        voice_id=voice,
        settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
)

def eleven_play(what_ai_said):
    audio = generate(
                api_key=config["elevenlabs_key"],
                text=what_ai_said,
                voice=voice,
                model='eleven_multilingual_v2',
        )
    play(audio)

def respond_to_text(what_user_said,convo_history,window):
    response = client.chat.completions.create(
    model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": config["initial_prompt"] + "\nFor reference, here is our conversation history: "+convo_history},
            {"role": "user", "content": what_user_said}
        ]
    )
    return response.choices[0].message.content

def record_and_transcribe():
    audio_text = ""
    with sr.Microphone() as source:
        
        audio_text = r.listen(source,timeout=2,phrase_time_limit=30)
        
    try:
        
        # using google speech recognition
        what_user_said = r.recognize_google(audio_text)
    except Exception as ExMsg:
         print ("record_and_transcribe:")
         print (ExMsg)
    if len(what_user_said) > 0:
        return what_user_said
    else:
        return -1

class Window(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        #self.layout = QVBoxLayout()
        self.layout = QGridLayout()
        self.setWindowTitle("Rue AI Labs")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.convo = QPlainTextEdit("")
        self.convo.setReadOnly(True)
        self.button1 = QPushButton('Record (30s)')
        self.button2 = QPushButton('Exit')
        self.button1.clicked.connect(self.record_button)
        self.button2.clicked.connect(self.quit_app)
        self.layout.addWidget(self.button1,0,0)
        self.layout.addWidget(self.button2,0,1)
        self.layout.addWidget(self.convo,1,0,1,4)
        self.setLayout(self.layout)
        self.setFixedSize(640,480)

    def update_convo_text(self):
        self.convo.setPlainText(convo_history)
        verScrollBar = self.convo.verticalScrollBar() 
        verScrollBar.setValue(verScrollBar.maximum())

    def record_button(self):
        if self.button1.text() == "Record (30s)":
            self.button1.setText("Recording")
            self.button1.setEnabled(False)
            self.repaint()
            self.update()
            do_stuff(self)

        if self.button1.text() == "Recording":
            pass

        if self.button1.text() == "Processing...":
            pass

    def stop_recording(self):
        self.button1.setText("Record (30s)")
        self.button1.setEnabled(True)
        self.repaint()
        self.update()

    def processing(self):
        self.button1.setText("Processing...")
        self.repaint()
        self.update()


    def quit_app(self):
        sys.exit()

def update_convo(who, what,window):
    global convo_history
    convo_history =  convo_history + "<" + who + "> "+what+"\n"
    window.update_convo_text()

def do_stuff(window):
    global convo_history
    
    try:
        what_user_said = record_and_transcribe()
        window.processing()
    except:
        what_user_said = -1
    if what_user_said != -1:
        update_convo(who="User",what=what_user_said,window=window)
        what_ai_said = respond_to_text(what_user_said,convo_history,window)
        update_convo(who="AI",what=what_ai_said,window=window)
        eleven_play(what_ai_said)
    window.stop_recording()
        
def main():
    global convo_history
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
main()
