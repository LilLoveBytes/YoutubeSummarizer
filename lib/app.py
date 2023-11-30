import sys, os
from PyQt6 import QtCore
from openai import OpenAI
from dotenv import load_dotenv
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QSplitter, QHBoxLayout, QVBoxLayout, QStatusBar)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from transcriber import get_video_transcript, summarize_transcript, TranscriptsDisabled

# pyqt6 framework can detect project folder
def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

class myApp(QWidget):
  def __init__(self, client):
    super().__init__()
    self.window_width, self.window_height = 700, 700
    self.setMinimumSize(self.window_width, self.window_height)
    self.setWindowTitle('Youtube Video Summarizer App')
    # self.setWindowIcon(QIcon('./icon.png'))
    self.client = client

    self.layout = {}
    self.layout['main'] = QVBoxLayout()
    self.setLayout(self.layout['main'])
    self.init_UI()
    self.config_signal()

  def init_UI(self):
    self.layout['video_id_entry'] = QHBoxLayout()
    self.layout['main'].addLayout(self.layout['video_id_entry'])
    self.video_id_input = QLineEdit()
    self.layout['video_id_entry'].addWidget(QLabel('Video ID:'))
    self.layout['video_id_entry'].addWidget(self.video_id_input)
    self.layout['video_id_entry'].addStretch(1)
    splitter = QSplitter(Qt.Orientation.Vertical)
    self.layout['main'].addWidget(splitter)

    self.transcription_field = QTextEdit()
    self.summarized_field = QTextEdit()
    splitter.addWidget(self.transcription_field)
    splitter.addWidget(self.summarized_field)

    # prevents splitter from being completely closed
    splitter.setCollapsible(0, False)
    splitter.setCollapsible(1, False)

    # add buttons
    self.layout['button'] = QHBoxLayout()
    self.layout['main'].addLayout(self.layout['button'])
    self.btn_transcribe = QPushButton('&Transcribe')
    self.btn_transcribe.setFixedWidth(100)
    self.btn_summarize = QPushButton('&Summarize')
    self.btn_summarize.setFixedWidth(100)
    self.btn_reset = QPushButton('&Reset')
    self.btn_reset.setFixedWidth(100)
    self.layout['button'].addWidget(self.btn_transcribe)
    self.layout['button'].addWidget(self.btn_summarize)
    self.layout['button'].addWidget(self.btn_reset)
    self.layout['button'].addStretch()

    # add status bar
    self.statusbar = QStatusBar()
    self.layout['main'].addWidget(self.statusbar)
  
  def reset_fields(self):
    self.video_id_input.clear()
    self.transcription_field.clear()
    self.summarized_field.clear()
    self.statusbar.clearMessage()

  def transcribe_video(self):
    video_id = self.video_id_input.text()
    if not video_id:
      self.statusbar.showMessage('Video ID is missing')
      return
    
    self.statusbar.clearMessage()
    self.transcription_field.clear()
    self.summarized_field.clear()

    try: 
      transcription = get_video_transcript(video_id)
      self.transcription_field.setPlainText(transcription)
    except TranscriptsDisabled:
      self.statusbar.showMessage('Transcription not available')
    except Exception as e:
      self.statusbar.showMessage(str(e))
      

  def summarize_video(self):
    transcription = self.transcription_field.toPlainText()
    if not transcription:
      self.statusbar.showMessage('Transcription is empty')
    self.summarized_field.clear()
    self.statusbar.clearMessage()

    try:
      video_summary = summarize_transcript(api_key_openai, transcription)
      self.summarized_field.setPlainText(video_summary)
    except Exception as e:
      # self.statusbar.showMessage(str(e))
      self.summarized_field.setPlainText(str(e))


  def config_signal(self):
    self.btn_transcribe.clicked.connect(self.transcribe_video)
    self.btn_summarize.clicked.connect(self.summarize_video)
    self.btn_reset.clicked.connect(self.reset_fields)



if __name__ == '__main__':
  load_dotenv()
  api_key_openai = os.getenv("OPENAI_API_KEY")
  client = OpenAI(
    api_key = api_key_openai
    )
  
  app = QApplication(sys.argv)

  myApp = myApp(client)
  myApp.show()

  try: 
    sys.exit(app.exec())
  except SystemExit:
    print('Closing Window...')