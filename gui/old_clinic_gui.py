import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtWidgets import QPushButton, QPlainTextEdit, QWidget

from clinic.controller import Controller
from .note_gui import NoteGUI

class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # Continue here with your code!
        self.controller = Controller(autosave=True)
        self.setWindowTitle("Patients")
        self.resize(600, 400)

        #just store as list for now
        self.patient_text_box = QPlainTextEdit()
        note_button = QPushButton("Note GUI")
        note_button.clicked.connect(self.get_patient_notes)
        
        #append elements to layout
        layout = QVBoxLayout()
        layout.addWidget(self.patient_text_box)
        layout.addWidget(note_button)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        #login for now
        self.controller.login('user', '123456')

        self.load_patients()
    
    def load_patients(self):
        #load list of patients
        patients = self.controller.list_patients()
        for patient in patients:
            self.patient_text_box.appendPlainText(str(patient))

    def get_patient_notes(self):
        #modify when patient table is set up
        #pass a random phn
        note_gui = NoteGUI(self.controller, 123) #bad to not have it as an instance variable?
        # note_gui.list_all_notes(123)
        note_gui.show()



def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
