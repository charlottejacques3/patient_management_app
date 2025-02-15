from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout

from clinic.controller import Controller

class DeleteNoteGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Delete Note")

        #create text boxes + labels
        code_label = QLabel("Enter Code of the Note to Delete:")
        self.code_text = QLineEdit()

        #create buttons
        self.cancel_button = QPushButton("Cancel")
        self.delete_button = QPushButton("Delete Note")
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        self.delete_button.clicked.connect(self.delete_button_clicked)

        #button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.delete_button)
        bottom_widget = QWidget()
        bottom_widget.setLayout(button_layout)

        #overall layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(code_label)
        main_layout.addWidget(self.code_text)
        main_layout.addWidget(bottom_widget)
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def delete_button_clicked(self):
        try:
            code = self.code_text.text()
            self.controller.delete_note(int(code))

            #sucess message 
            msg = QMessageBox()
            msg.setText("Note deleted successfully")
            msg.exec()

            #refresh note list
            self.parent.note_list.setPlainText("")
            self.parent.list_all_notes()
            self.cancel_button_clicked()
        except:
            msg = QMessageBox()
            msg.setText("Failed to delete note")
            msg.exec()
            self.clear()

    def cancel_button_clicked(self):
        self.clear()
        self.hide()

    def clear(self):
        self.code_text.setText("")