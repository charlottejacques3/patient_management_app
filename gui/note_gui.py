from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QPlainTextEdit
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QFormLayout

from clinic.controller import Controller
from .add_note_gui import AddNoteGUI
from .update_note_gui import UpdateNoteGUI
from .delete_note_gui import DeleteNoteGUI

from datetime import datetime

from clinic.exception.illegal_operation_exception import IllegalOperationException

class NoteGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.note_list = QPlainTextEdit()
        
        self.setWindowTitle("Notes")
        self.resize(600, 400)

        # ENTER PHN WIDGET ------------------------------------------------------------------------------------

        phn_label = QLabel("Enter PHN")
        self.phn_text = QLineEdit()

        submit_button = QPushButton("Start Appointment")
        submit_button.clicked.connect(self.submit_button_clicked)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel_button_clicked)

        enter_phn_layout = QFormLayout()
        enter_phn_layout.setSpacing(30)
        enter_phn_layout.setContentsMargins(50, 100, 50, 50)
        enter_phn_layout.addRow(phn_label, self.phn_text)

        #submit button
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(submit_button)
        button_widget.setLayout(button_layout)
        enter_phn_layout.addRow(button_widget)

        enter_phn_widget = QWidget()
        enter_phn_widget.setLayout(enter_phn_layout)


        # SHOW NOTES FOR A SPECIFIC PATIENT WIDGET -------------------------------------------------------------
        
        #add note function
        self.add_note_gui = AddNoteGUI(self.controller, self)
        add_button = QPushButton("Add Note")
        add_button.clicked.connect(self.add_button_clicked)

        #update note function
        self.update_note_gui = UpdateNoteGUI(self.controller, self)
        update_button = QPushButton("Update a Note")
        update_button.clicked.connect(self.update_button_clicked)

        #delete note function
        self.delete_note_gui = DeleteNoteGUI(self.controller, self)
        delete_button = QPushButton("Delete a Note")
        delete_button.clicked.connect(self.delete_button_clicked)

        #button layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        bottom_widget = QWidget()
        bottom_widget.setLayout(button_layout)

        #search function
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search Notes")
        search_button = QPushButton("Search")
        reset_button = QPushButton("Reset")
        search_button.clicked.connect(self.search_button_clicked)
        reset_button.clicked.connect(self.reset_button_clicked)

        #search layout
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search)
        search_layout.addWidget(search_button)
        search_layout.addWidget(reset_button)
        top_widget = QWidget()
        top_widget.setLayout(search_layout)

        #append elements to main layout
        layout = QVBoxLayout()
        layout.addWidget(top_widget)
        layout.addWidget(self.note_list)
        layout.addWidget(bottom_widget)
        self.main_widget = QWidget()
        self.main_widget.setLayout(layout)
        # self.setCentralWidget(widget)

        #set up
        # self.list_all_notes()

        # SET APPROPRIATE LAYOUT -----------------------------------------------------
        self.widget = QStackedWidget()
        self.widget.addWidget(enter_phn_widget)
        self.widget.addWidget(self.main_widget)

        self.widget.setCurrentWidget(enter_phn_widget)
        self.setCentralWidget(self.widget)
    
    def list_notes(self, notes):
        for note in notes:
            date_str = note.timestamp.strftime("%d/%m/%Y")
            self.note_list.appendPlainText("(Note %d, %s) %s" % (note.code, date_str, note.text))

    def list_all_notes(self):
        notes = self.controller.list_notes()
        self.list_notes(notes)

    def add_button_clicked(self):
        self.add_note_gui.show()

    def search_button_clicked(self):
        search_text = self.search.text()
        search_results = self.controller.retrieve_notes(search_text)
        self.note_list.setPlainText("") #reset text
        self.list_notes(search_results)

    def reset_button_clicked(self):
        self.note_list.setPlainText("")
        self.search.setText("")
        self.list_all_notes()

    def update_button_clicked(self):
        self.update_note_gui.show()
        
    def delete_button_clicked(self):
        self.delete_note_gui.show()


    # ENTER PHN FUNCTIONS ----------------------------------------------------------------

    def submit_button_clicked(self):
        phn = int(self.phn_text.text())
        try:
            self.controller.set_current_patient(phn)

            #change the widget
            self.widget.setCurrentWidget(self.main_widget)
            self.list_all_notes()
        except IllegalOperationException:
            #invalid phn dialog
            msg = QMessageBox()
            msg.setText("This PHN does not exist")
            msg.exec()

            #clear
            self.phn_text.setText("")

    def cancel_button_clicked(self):
        self.close()