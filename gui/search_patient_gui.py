import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from clinic.controller import Controller, IllegalOperationException

class SearchPatientGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()

        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Search Patient")

        layout1 = QGridLayout()

        label_phn = QLabel("Patient PHN")
        self.text_phn = QLineEdit()
        self.text_phn.setInputMask('0000000000')
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
        self.button_search = QPushButton("Search by PHN")
        self.button_close = QPushButton("Close")
        layout2.addWidget(self.button_clear)
        layout2.addWidget(self.button_search)
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
        self.text_name.setEnabled(False)
        self.text_birth_date.setEnabled(False)
        self.text_email.setEnabled(False)
        self.text_phone.setEnabled(False)
        self.text_address.setEnabled(False)

        self.button_clear.setEnabled(True)
        self.button_search.setEnabled(False)
        self.button_close.setEnabled(True)

        # handle text change to enable/disable the create button
        self.text_phn.textChanged.connect(self.patient_phn_changed)

        # connect the buttons' clicked signals to the slots below
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_search.clicked.connect(self.search_button_clicked)
        self.button_close.clicked.connect(self.close_button_clicked)

    def patient_phn_changed(self):
        if self.text_phn.text():
            self.button_search.setEnabled(True)
        else:
            self.button_search.setEnabled(False)

    def clear_button_clicked(self):
        ''' clear the fields '''
        self.text_phn.setText("")
        self.text_name.setText("")
        self.text_birth_date.setText("")
        self.text_email.setText("")
        self.text_phone.setText("")
        self.text_address.setText("")

        self.text_phn.setEnabled(True)
        # self.text_name.setEnabled(True)
        # self.text_birth_date.setEnabled(True)
        # self.text_email.setEnabled(True)
        # self.text_phone.setEnabled(True)
        # self.text_address.setEnabled(True)

    def search_button_clicked(self):
        '''search for patient with phn'''
        patient_phn = int(self.text_phn.text())
        patient = self.controller.search_patient(patient_phn)

        if patient:
            
            self.text_name.setText(str(patient.name))
            self.text_phn.setText(str(patient.phn))
            self.text_birth_date.setText(str(patient.birth_date))
            self.text_email.setText(str(patient.email))
            self.text_phone.setText(str(patient.phone))
            self.text_address.setText(str(patient.address))
            
            # make widgets read-only
            self.text_phn.setEnabled(False)

            # TODO: if you have not found a product, show a warning message and clear the fields afterwards

        else:
            dialogue = QMessageBox(self)
            dialogue.warning(self,"Patient DNE", "There is no patient with that code.")

            self.text_phn.setText("")

    def close_button_clicked(self):
        ''' 'close add patient window '''
        # Notice that it is important to clear the QLineEdits when this window is
        # closed, so they will come back clean when the window is reopened.
        self.clear_button_clicked()
        
        self.hide()

    def closeEvent(self, event):
        self.close_button_clicked()