import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from clinic.controller import Controller, IllegalOperationException


class UpdatePatientGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Update Patient")

        layout1 = QGridLayout()

        label_og_phn = QLabel("Patient OG PHN")
        self.text_og_phn = QLineEdit()
        self.text_og_phn.setInputMask('0000000000')
        label_new_phn = QLabel("Patient New PHN")
        self.text_new_phn = QLineEdit()
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

        layout1.addWidget(label_og_phn, 0, 0)
        layout1.addWidget(self.text_og_phn, 0, 1)
        layout1.addWidget(label_new_phn, 1, 0)
        layout1.addWidget(self.text_new_phn, 1, 1)
        layout1.addWidget(label_name, 2, 0)
        layout1.addWidget(self.text_name, 2, 1)
        layout1.addWidget(label_birth_date, 3, 0)
        layout1.addWidget(self.text_birth_date, 3, 1)
        layout1.addWidget(label_phone, 4, 0)
        layout1.addWidget(self.text_phone, 4, 1)
        layout1.addWidget(label_email, 5, 0)
        layout1.addWidget(self.text_email, 5, 1)
        layout1.addWidget(label_address, 6, 0)
        layout1.addWidget(self.text_address, 6, 1)

        layout2 = QHBoxLayout()

        self.button_search = QPushButton("Search")
        self.button_clear = QPushButton("Clear")
        self.button_update = QPushButton("Update")
        self.button_close = QPushButton("Close")
        layout2.addWidget(self.button_search)
        layout2.addWidget(self.button_clear)
        layout2.addWidget(self.button_update)
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
        self.text_og_phn.setEnabled(True)
        self.text_new_phn.setEnabled(False)
        self.text_name.setEnabled(False)
        self.text_birth_date.setEnabled(False)
        self.text_email.setEnabled(False)
        self.text_phone.setEnabled(False)
        self.text_address.setEnabled(False)

        self.button_search.setEnabled(False)
        self.button_clear.setEnabled(True)
        self.button_update.setEnabled(False)
        self.button_close.setEnabled(True)

        # handle text change to enable/disable the update button
        self.text_og_phn.textChanged.connect(self.phn_changed)

        # connect the buttons' clicked signals to the slots below
        self.button_search.clicked.connect(self.search_button_clicked)
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_update.clicked.connect(self.update_button_clicked)
        self.button_close.clicked.connect(self.close_button_clicked)

    def phn_changed(self):
        if self.text_og_phn.text():
            self.button_search.setEnabled(True)
        else:
            self.button_search.setEnabled(False)

    def clear_button_clicked(self):
        ''' clear the fields '''
        # TODO: Clear all the QLineEdits' text.

        self.text_og_phn.setText("")
        self.text_new_phn.setText("")
        self.text_name.setText("")
        self.text_birth_date.setText("")
        self.text_phone.setText("")
        self.text_email.setText("")
        self.text_address.setText("")

    def search_button_clicked(self):
        patient_phn = int(self.text_og_phn.text())
        patient = self.controller.search_patient(patient_phn)

        if patient:
            
            self.text_name.setText(str(patient.name))
            self.text_new_phn.setText(str(patient.phn))
            self.text_birth_date.setText(str(patient.birth_date))
            self.text_email.setText(str(patient.email))
            self.text_phone.setText(str(patient.phone))
            self.text_address.setText(str(patient.address))

            self.button_update.setEnabled(True)

            self.text_new_phn.setEnabled(True)
            self.text_name.setEnabled(True)
            self.text_birth_date.setEnabled(True)
            self.text_email.setEnabled(True)
            self.text_phone.setEnabled(True)
            self.text_address.setEnabled(True)


        else:
            dialogue = QMessageBox(self)
            dialogue.warning(self,"Patient DNE", "There is no patient with that code.")

            self.text_og_phn.setText("")

    def update_button_clicked(self):
        ''' update new patient '''
        try:
            og_phn = int(self.text_og_phn.text())
            new_phn = int(self.text_new_phn.text())
            new_name = self.text_name.text()
            new_birth_date = self.text_birth_date.text()
            new_phone = self.text_phone.text()
            new_email = self.text_email.text()
            new_address = self.text_address.text()

            self.controller.update_patient(og_phn, new_phn, new_name, new_birth_date, new_phone, new_email, new_address)

            dialogue = QMessageBox(self)
            dialogue.information(self, "Success", "Patient successfully updated!")

            # After a patient is created, the original parent window with the table 
            # needs to be updated, refreshing the table data from the patients' storage.   
            self.parent.refresh_table()
            self.close_button_clicked()

        except IllegalOperationException:
            # TODO: Show a message with an error when adding a patient with an existing code.
            dialogue = QMessageBox(self)
            dialogue.warning(self, "Warning message", "Patient is current patient")

            # clear the buttons

    def close_button_clicked(self):
        ''' 'close add patient window '''
        # Notice that it is important to clear the QLineEdits when this window is
        # closed, so they will come back clean when the window is reopened.
        self.clear_button_clicked()
        self.hide()

    def closeEvent(self, event):
        self.close_button_clicked()