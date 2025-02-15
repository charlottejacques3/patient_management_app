import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from clinic.controller import Controller, IllegalOperationException


class RemovePatientGUI(QMainWindow):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Remove Patient")

        layout1 = QGridLayout()

        label_phn = QLabel("Patient PHN")
        self.text_phn = QLineEdit()
        self.text_phn.setInputMask('0000000000')

        layout1.addWidget(label_phn, 0, 0)
        layout1.addWidget(self.text_phn, 0, 1)

        layout2 = QHBoxLayout()
        self.button_clear = QPushButton("Clear")
        self.button_remove = QPushButton("Search by PHN")
        self.button_close = QPushButton("Close")
        layout2.addWidget(self.button_clear)
        layout2.addWidget(self.button_remove)
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

        self.text_phn.setEnabled(True)

        self.button_clear.setEnabled(True)
        self.button_remove.setEnabled(False)
        self.button_close.setEnabled(True)

        self.text_phn.textChanged.connect(self.patient_phn_changed)

        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_remove.clicked.connect(self.remove_button_clicked)
        self.button_close.clicked.connect(self.close_button_clicked)

    def patient_phn_changed(self):
        if self.text_phn.text():
            self.button_remove.setEnabled(True)
        else:
            self.button_remove.setEnabled(False)

    def clear_button_clicked(self):
        ''' clear the fields '''
        self.text_phn.setText("")

    def remove_button_clicked(self):
        try:
            patient_phn = int(self.text_phn.text())
            patient = self.controller.delete_patient(patient_phn)

            dialogue = QMessageBox(self)
            dialogue.information(self,"Patient Removed", "Patient successfully removed.")

            self.clear_button_clicked()

            self.parent.refresh_table()
            self.close_button_clicked()

        except IllegalOperationException:
            dialogue = QMessageBox(self)
            dialogue.warning(self, "Warning message", "Patient can't be deleted")


    def close_button_clicked(self):
        ''' 'close add patient window '''
        # Notice that it is important to clear the QLineEdits when this window is
        # closed, so they will come back clean when the window is reopened.
        self.clear_button_clicked()
        
        self.hide()

    def closeEvent(self, event):
        self.close_button_clicked()