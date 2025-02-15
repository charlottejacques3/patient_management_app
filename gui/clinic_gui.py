import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFormLayout, QHBoxLayout
from PyQt6.QtWidgets import QPushButton, QTableView, QWidget, QLabel, QLineEdit, QStackedWidget, QMessageBox

from clinic.controller import Controller
from clinic.patient import Patient
from clinic.gui.patient_table_model import PatientTableModel

from clinic.gui.add_patient_gui import AddPatientGUI
from clinic.gui.search_patient_gui import SearchPatientGUI
from clinic.gui.update_patient_gui import UpdatePatientGUI
from clinic.gui.remove_patient_gui import RemovePatientGUI

from .note_gui import NoteGUI

from clinic.exception.invalid_login_exception import InvalidLoginException

class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # Continue here with your code!
        
        self.controller = Controller(autosave=True)
        self.setWindowTitle("Patients")
        self.resize(650, 500)

        # LOGIN WIDGET ---------------------------------------------------------------------------

        user_label = QLabel("Username")
        self.user_text = QLineEdit()
        pw_label = QLabel("Password")
        self.pw_text = QLineEdit()
        self.pw_text.setEchoMode(QLineEdit.EchoMode.Password) #only show as ellipses

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login_button_clicked)

        login_layout = QFormLayout()
        login_layout.setSpacing(30)
        login_layout.setContentsMargins(50, 100, 50, 50)
        login_layout.addRow(user_label, self.user_text)
        login_layout.addRow(pw_label, self.pw_text)

        #login button
        button_widget = QWidget()
        button_layout = QVBoxLayout()
        button_layout.addWidget(login_button)
        button_widget.setLayout(button_layout)
        login_layout.addRow(button_widget)

        self.login_widget = QWidget()
        self.login_widget.setLayout(login_layout)


        # PATIENT WIDGET -------------------------------------------------------------------------

        self.add_button = QPushButton("Add Patient")
        self.add_button.clicked.connect(self.add_button_clicked)

        self.search_button = QPushButton("Search Patient")
        self.search_button.clicked.connect(self.search_button_clicked)

        self.update_button = QPushButton("Update Patient")
        self.update_button.clicked.connect(self.update_button_clicked)

        self.remove_button = QPushButton("Remove Patient")
        self.remove_button.clicked.connect(self.remove_button_clicked)

        self.note_button = QPushButton("Start Appointment")
        self.note_button.clicked.connect(self.get_patient_notes)

        self.logout_button = QPushButton("Log Out")
        self.logout_button.clicked.connect(self.logout_button_clicked)

        #search function
        self.retrieve = QLineEdit()
        self.retrieve.setPlaceholderText("Retrieve Patient by Name")
        retrieve_button = QPushButton("Retrieve")
        reset_button = QPushButton("Reset")
        retrieve_button.clicked.connect(self.retrieve_button_clicked)
        reset_button.clicked.connect(self.reset_button_clicked)

        #search layout
        retrieve_layout = QHBoxLayout()
        retrieve_layout.addWidget(self.retrieve)
        retrieve_layout.addWidget(retrieve_button)
        retrieve_layout.addWidget(reset_button)
        top_widget = QWidget()
        top_widget.setLayout(retrieve_layout)

        # add sub windows
        self.add_patient_gui = AddPatientGUI(self.controller, parent=self)
        self.search_patient_gui = SearchPatientGUI(self.controller, parent=self)
        self.update_patient_gui = UpdatePatientGUI(self.controller, parent=self)
        self.remove_patient_gui = RemovePatientGUI(self.controller, parent=self)

        self.patient_table = QTableView()

        layout = QVBoxLayout()
        layout.addWidget(top_widget)
        layout.addWidget(self.patient_table)
        layout.addWidget(self.add_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.note_button)
        layout.addWidget(self.logout_button)

        self.patient_widget = QWidget()
        self.patient_widget.setLayout(layout)
        self.setCentralWidget(self.patient_widget)

        # SET APPROPRIATE LAYOUT -----------------------------------------------------
        self.widget = QStackedWidget()
        self.widget.addWidget(self.login_widget)
        self.widget.addWidget(self.patient_widget)

        self.widget.setCurrentWidget(self.login_widget)
        self.setCentralWidget(self.widget)

    def refresh_table(self):
        self.patient_model.refresh_data()
        self.patient_table.setColumnWidth(1, 200)
        self.patient_table.setEnabled(True)

    def add_button_clicked(self):
        self.add_patient_gui.show()

    def search_button_clicked(self):
        self.search_patient_gui.show()

    def update_button_clicked(self):
        self.update_patient_gui.show()

    def retrieve_button_clicked(self):
        name_to_search = self.retrieve.text()
        self.patient_model.retrieve_button_clicked(name_to_search)

    def reset_button_clicked(self):
        self.patient_model.reset_button_clicked()
        self.retrieve.setText("")

    def remove_button_clicked(self):
        self.remove_patient_gui.show()
    
    def get_patient_notes(self):
        #open note gui
        note_gui = NoteGUI(self.controller, self)
        note_gui.show()

    def login_button_clicked(self):
        user = self.user_text.text()
        pw = self.pw_text.text()
        try:
            self.controller.login(user, pw)

            #set the model
            self.patient_model = PatientTableModel(self.controller)
            self.patient_table.setModel(self.patient_model)

            #change the widget
            self.widget.setCurrentWidget(self.patient_widget)
            self.refresh_table()

        except InvalidLoginException:

            #invalid login dialog
            msg = QMessageBox()
            msg.setText("Invalid login")
            msg.exec()

        #clear login fields
        self.user_text.setText("")
        self.pw_text.setText("")
    
    def logout_button_clicked(self):
        self.controller.logout()

        #bring back to login widget
        self.widget.setCurrentWidget(self.login_widget)



def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
