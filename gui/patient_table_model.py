import sys
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import QPushButton, QLineEdit

from clinic.controller import Controller
from clinic.patient import Patient

class PatientTableModel(QAbstractTableModel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._data = []
        self.refresh_data()

    def refresh_data(self):
        self._data = []

        patient_list = self.controller.list_patients()

        index = 0
        for patient in patient_list:
            cur_patient = [patient.phn, patient.name, patient.birth_date, patient.phone, patient.email, patient.address]
            self._data.append(cur_patient)
        
        # emit the layoutChanged signal to alert the QTableView of model changes
        self.layoutChanged.emit()

    def retrieve_button_clicked(self, name_to_search):
        #search_text = self.search.text()
        search_results = self.controller.retrieve_patients(name_to_search)
        self._data = [] #reset patients
        self.list_patients(search_results)
        
        self.layoutChanged.emit()

    def reset_button_clicked(self):
        self._data = [] #reset patients
        all_patients = self.controller.list_patients()
        self.list_patients(all_patients)

        self.layoutChanged.emit()

    def list_patients(self, patients):
        for patient in patients:
            cur_patient = [patient.phn, patient.name, patient.birth_date, patient.phone, patient.email, patient.address]
            self._data.append(cur_patient)

    def reset(self):
        self._data = []
        # emit the layoutChanged signal to alert the QTableView of model changes
        self.layoutChanged.emit()

    def data(self, index, role):
        value = self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            # Perform per-type checks and render accordingly.
            if isinstance(value, str):
                # Render strings with quotes
                return '%s' % value
            # Default (anything not captured above: e.g. int)
            return value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if isinstance(value, int) or isinstance(value, float):
                # Align right, vertical middle.
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        if self._data:
            return len(self._data[0])
        else:
            return 0

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        headers = ['PHN', 'Name', 'DOB', 'Phone', 'Email', 'Address']
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return '%s' % headers[section]
        return super().headerData(section, orientation, role)

    