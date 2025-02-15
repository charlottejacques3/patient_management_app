from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QPushButton, QMessageBox, QTextEdit
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout

from clinic.controller import Controller
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class AddNoteGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Add Note")

        #create text box
        self.text_box = QTextEdit()

        #create buttons
        self.clear_button = QPushButton("Clear")
        self.cancel_button = QPushButton("Cancel")
        self.add_button = QPushButton("Add Note")
        self.clear_button.clicked.connect(self.clear_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        self.add_button.clicked.connect(self.add_button_clicked)

        #button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.add_button)
        bottom_widget = QWidget()
        bottom_widget.setLayout(button_layout)

        #overall layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.text_box)
        main_layout.addWidget(bottom_widget)
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
    
    def add_button_clicked(self):
        try:
            text = self.text_box.toPlainText()
            self.controller.create_note(text)

            #sucess message 
            msg = QMessageBox()
            msg.setText("Note created successfully!")
            msg.exec()

            #refresh note list
            self.parent.note_list.setPlainText("")
            self.parent.list_all_notes()
            self.cancel_button_clicked()
        except:
            msg = QMessageBox()
            msg.setText("Failed to create note")
            msg.exec()
            self.clear_button_clicked()

    def clear_button_clicked(self):
        self.text_box.setText("")
    
    def cancel_button_clicked(self):
        self.clear_button_clicked()
        self.hide()
        