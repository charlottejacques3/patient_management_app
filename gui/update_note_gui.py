from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout

from clinic.controller import Controller

class UpdateNoteGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Update Note")

        #create text boxes + labels
        code_label = QLabel("Enter Code of the Note to Update:")
        self.code_text = QLineEdit()
        text_label = QLabel("Updated Note:")
        self.new_text = QTextEdit()

        #create buttons
        self.cancel_button = QPushButton("Cancel")
        self.update_button = QPushButton("Update Note")
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        self.update_button.clicked.connect(self.update_button_clicked)

        #button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.update_button)
        bottom_widget = QWidget()
        bottom_widget.setLayout(button_layout)

        #overall layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(code_label)
        main_layout.addWidget(self.code_text)
        main_layout.addWidget(text_label)
        main_layout.addWidget(self.new_text)
        main_layout.addWidget(bottom_widget)
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def update_button_clicked(self):
        try:
            code = self.code_text.text()
            text = self.new_text.toPlainText()
            self.controller.update_note(int(code), text)

            #sucess message 
            msg = QMessageBox()
            msg.setText("Note updated successfully")
            msg.exec()

            #refresh note list
            self.parent.note_list.setPlainText("")
            self.parent.list_all_notes()
            self.cancel_button_clicked()
        except:
            msg = QMessageBox()
            msg.setText("Failed to update note")
            msg.exec()
            self.clear()

    def cancel_button_clicked(self):
        self.clear()
        self.hide()

    def clear(self):
        self.code_text.setText("")
        self.new_text.setPlainText("")