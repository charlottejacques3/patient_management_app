import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from clinic.controller import Controller, IllegalOperationException


class AddPatientGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Add Patient")

        layout1 = QGridLayout()

        label_phn = QLabel("Patient PHN")
        self.text_phn = QLineEdit()
        self.text_phn.setInputMask('000000000')
        label_name = QLabel("Name")
        self.text_name = QLineEdit()
        label_birth_date = QLabel("Birthdate")
        self.text_birth_date = QLineEdit()
        label_phone = QLabel("Phone Number")
        self.text_phone = QLineEdit()
        label_email = QLabel("Email")
        self.text_email = QLineEdit()
        label_address = QLabel("Address")
        self.text_address = QLineEdit()

        layout1.addWidget(label_phn, 0, 0)
        layout1.addWidget(self.text_phn, 0, 1)
        layout1.addWidget(label_name, 1, 0)
        layout1.addWidget(self.text_name, 1, 1)
        layout1.addWidget(label_birth_date, 2, 0)
        layout1.addWidget(self.text_birth_date, 2, 1)
        layout1.addWidget(label_phone, 3, 0)
        layout1.addWidget(self.text_phone, 3, 1)
        layout1.addWidget(label_email, 4, 0)
        layout1.addWidget(self.text_email, 4, 1)
        layout1.addWidget(label_address, 5, 0)
        layout1.addWidget(self.text_address, 5, 1)

        layout2 = QHBoxLayout()

        self.button_clear = QPushButton("Clear")
        self.button_create = QPushButton("Add")
        self.button_close = QPushButton("Close")
        layout2.addWidget(self.button_clear)
        layout2.addWidget(self.button_create)
        layout2.addWidget(self.button_close)

        layout3 = QVBoxLayout()

        top_widget = QWidget()
        top_widget.setLayout(layout1)
        bottom_widget = QWidget()
        bottom_widget.setLayout(layout2)
        layout3.addWidget(top_widget)
        layout3.addWidget(bottom_widget)
        widget = QWidget()
        widget.setLayout(layout3)

        self.setCentralWidget(widget)

        # define widgets' initial state
        self.text_phn.setEnabled(True)
        self.text_name.setEnabled(True)
        self.text_birth_date.setEnabled(True)
        self.text_email.setEnabled(True)
        self.text_phone.setEnabled(True)
        self.text_address.setEnabled(True)

        self.button_clear.setEnabled(True)
        self.button_create.setEnabled(False)
        self.button_close.setEnabled(True)

        # handle text change to enable/disable the create button
        
        self.text_phn.textChanged.connect(self.patient_text_changed)
        self.text_name.textChanged.connect(self.patient_text_changed)
        self.text_birth_date.textChanged.connect(self.patient_text_changed)
        self.text_email.textChanged.connect(self.patient_text_changed)
        self.text_phone.textChanged.connect(self.patient_text_changed)
        self.text_address.textChanged.connect(self.patient_text_changed)

        # connect the buttons' clicked signals to the slots below
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_create.clicked.connect(self.create_button_clicked)
        self.button_close.clicked.connect(self.close_button_clicked)

    def patient_text_changed(self):
        if self.text_phn.text() and self.text_name.text() \
            and self.text_birth_date.text() and self.text_phone.text() \
            and self.text_email.text() and self.text_address.text():
            self.button_create.setEnabled(True)
        else:
            self.button_create.setEnabled(False)

    def clear_button_clicked(self):
        ''' clear the fields '''
        # TODO: Clear all the QLineEdits' text.

        self.text_phn.setText("")
        self.text_name.setText("")
        self.text_birth_date.setText("")
        self.text_phone.setText("")
        self.text_email.setText("")
        self.text_address.setText("")


    def create_button_clicked(self):
        ''' add new patient '''
        try:
            # TODO: Recover the patient data from the QLineEdits and store them
            # in local variables. You may have to do some conversions.
            # Then, call controller.create_patient() to add the new patient.
            # After successful creation, show an information message of success,
            # close this Add patients window.

            new_phn = int(self.text_phn.text())
            new_name = self.text_name.text()
            new_birth_date = self.text_birth_date.text()
            new_phone = self.text_phone.text()
            new_email = self.text_email.text()
            new_address = self.text_address.text()

            self.controller.create_patient(new_phn, new_name, new_birth_date, new_phone, new_email, new_address)

            dialogue = QMessageBox(self)
            dialogue.information(self, "Success", "Patient successfully added!")


            # After a patietn is created, the original parent window with the table 
            # needs to be updated, refreshing the table data from the patients' storage.   
            self.parent.refresh_table()
            self.close_button_clicked()

        except IllegalOperationException:
            # TODO: Show a message with an error when adding a patient with an existing code.
            dialogue = QMessageBox(self)
            dialogue.warning(self, "Warning message", "PHN already registered")

            # clear the buttons

    def close_button_clicked(self):
        ''' 'close add patient window '''
        # Notice that it is important to clear the QLineEdits when this window is
        # closed, so they will come back clean when the window is reopened.
        self.clear_button_clicked()
        self.hide()

    def closeEvent(self, event):
        self.close_button_clicked()