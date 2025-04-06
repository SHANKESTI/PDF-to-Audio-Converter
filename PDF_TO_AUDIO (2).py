# Import necessary modules
import os
import PyPDF2
import pyttsx3
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication
from PyQt5.QtWidgets import QMessageBox

def convert_pdf_to_audio():
    # Ask the user to select a PDF file
    pdf_file_path, _ = QFileDialog.getOpenFileName(None, "Select PDF File", "", "PDF Files (*.pdf)")

    # Get the user-selected audio duration in minutes and convert it to the number of words
    duration = int(entry_duration.text())  # Duration in minutes
    words_per_minute = 135  # Average words per minute
    words_per_chunk = duration * words_per_minute

    # Ask the user for the playlist directory
    playlist_dir = QFileDialog.getExistingDirectory(None, "Choose Playlist Directory")

    # Read the PDF content
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        full_text = ""
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            full_text += page.extract_text()

    # Split the text into chunks of approximately words_per_chunk words each
    words = full_text.split()
    chunks = [' '.join(words[i:i + words_per_chunk]) for i in range(0, len(words), words_per_chunk)]

    # Get the base name of the PDF file (without extension) and replace spaces with underscores
    base_name = os.path.basename(pdf_file_path)
    base_name = os.path.splitext(base_name)[0].replace(' ', '_')

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set the default speed of the audio to 1x
    engine.setProperty('rate', 125)

    # Set the voice (change index for different voices)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Try 0 or 1 or higher depending on available voices

    # Convert each chunk of text to audio using pyttsx3
    for i, chunk in enumerate(chunks):
        mp3_file_name = f"{base_name}_{i + 1}.mp3"
        mp3_file_path = os.path.join(playlist_dir, mp3_file_name)
        engine.save_to_file(chunk, mp3_file_path)

    engine.runAndWait()

    # Show a message box when the conversion is complete
    msg = QMessageBox()
    msg.setTextFormat(QtCore.Qt.RichText)
    msg.setText("<div style='background-color: #f2f2f2; padding: 20px; border: 2px solid black; border-radius: 5px;'>"
                "<h2 style='color: green;'>Conversion Complete</h2>"
                "<p style='color: blue;'>The PDF has been successfully converted to audio.</p>"
                "</div>")
    msg.setWindowTitle("Conversion Complete")
    msg.exec_()

# Create a QApplication
app = QtWidgets.QApplication([])

# Create a window
window = QtWidgets.QWidget()
window.setWindowTitle("PDF to Audio Converter")
window.setStyleSheet("background-color: #2e2e2e; color: #ffffff; padding: 20px;")

# Create a main layout with reduced spacing
main_layout = QtWidgets.QVBoxLayout()
main_layout.setSpacing(10)

# Greeting label with emoji
greeting_layout = QtWidgets.QHBoxLayout()
greeting_label = QtWidgets.QLabel("📚🔊 Welcome to the PDF to Audio Converter! 📚🔊")
greeting_label.setFont(QtGui.QFont('Segoe UI', 24, QtGui.QFont.Bold))
greeting_layout.addStretch()
greeting_layout.addWidget(greeting_label)
greeting_layout.addStretch()
main_layout.addLayout(greeting_layout)

# Label and Entry for audio duration input
duration_label = QtWidgets.QLabel("Enter duration of the audio in minutes:")
duration_label.setFont(QtGui.QFont('Segoe UI', 20, QtGui.QFont.Bold))
entry_duration = QtWidgets.QLineEdit()
entry_duration.setFont(QtGui.QFont('Courier New', 20))
entry_duration.setFixedWidth(400)
entry_duration.setStyleSheet("background-color:black ; padx:12px; pady:12px; border: 4px solid white; border-radius:12px")

form_layout = QtWidgets.QFormLayout()
form_layout.addRow(duration_label, entry_duration)
main_layout.addLayout(form_layout)

# Button to trigger conversion
convert_button = QtWidgets.QPushButton("Choose PDF file and Convert to Audio")
convert_button.setFont(QtGui.QFont('Segoe UI', 22, QtGui.QFont.Bold))
convert_button.setStyleSheet("background-color: black; color: white; padding: 10px; border: 4px solid white ; border-radius:23px")
convert_button.setFixedWidth(600)
convert_button.setFixedHeight(75)
convert_button.clicked.connect(convert_pdf_to_audio)
main_layout.addWidget(convert_button, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)

# Notice label
notice_label = QtWidgets.QLabel("Note: This converter can only convert English language PDFs to audio.")
notice_label.setFont(QtGui.QFont('Segoe UI', 20, QtGui.QFont.Bold))
notice_label.setStyleSheet("color: red; padding:10px; border:4px solid white; border-radius:23px")
main_layout.addWidget(notice_label, alignment=QtCore.Qt.AlignCenter)

# Set layout and show window
window.setLayout(main_layout)
window.showMaximized()
app.exec_()
