from datetime import datetime, time
from PyQt5.QtWidgets import QDialog
from views.ui_confirmationDialog import Ui_ConfirmationDialog
from controllers.singleton import MongoManager
import pprint

def waterOnlyCheck(checkbox, rental, machine, nMachines):
    if checkbox.isChecked():
        rental.setEnabled(False)
        machine.setEnabled(False)
        nMachines.setEnabled(False)
    else:
        rental.setEnabled(True)
        machine.setEnabled(True)
        nMachines.setEnabled(True)

def accountCheck(ui):
    if ui.account.isChecked():
        ui.bill_address.insert(ui.address.text())
        ui.bill_city.insert(ui.city.text())
        ui.bill_region.insert(ui.region.text())
        ui.bill_postal_code.insert(ui.postal_code.text())

# Would be a good idea to do some validations in a future, like validating the essenstials by making them required

def createClient(self):

    # Get connection
    db = MongoManager.getInstance()
    collection = db.clients

    # Basic info
    client = {
        'name': self.ui.name.text(),
        'email': self.ui.email.text(),
        'phone_number': self.ui.phone_number.text(),
        'address': self.ui.address.text(),
        'city': self.ui.city.text(),
        'region': self.ui.region.text(),
        'postal_code': self.ui.postal_code.text(),
        'note': self.ui.note.text(),
        'billing': "",
        'contact_person': ""
    }

    #Account info
    if self.ui.account.isChecked():
        aux = {
            'billing': {
                'address': self.ui.bill_address.text(),
                'city': self.ui.bill_city.text(),
                'region': self.ui.bill_region.text(),
                'postal_code': self.ui.bill_postal_code.text()
            },
            'contact_person': self.ui.contact_person.text()
        }
        client.update(aux)

    # Additional info
    date = self.ui.first_visit.date().toPyDate()
    first_visit = datetime.combine(date, time.min) 

    clientAux = {
        'first_visit': first_visit,
        'water_price': self.ui.water_price.value(),
        'rental_price': "",
        'bottles_in_pos': self.ui.bottles_in_pos.value(),
        'machines_in_pos': "",
        'machine_type': "",
        'method_contact': self.ui.method_contact.text(),
        'lang': self.ui.lang.text()
    }

    if not self.ui.water_only.isChecked():
        aux = {
            'rental_price': self.ui.rental_price.value(),
            'machine_type': self.ui.machine_type.text(),
            'machines_in_pos': self.ui.machines_in_pos.value()
        }
        clientAux.update(aux)
    
    client.update(clientAux)

    # Validate the content


    result = collection.insert_one(client)
    #pprint.pprint('New client: {0}'.format(result.inserted_id))
    
    # Confirmation Dialog
    dialog = QDialog()
    dialog.ui = Ui_ConfirmationDialog()
    msg = "Succesfully added!"
    dialog.ui.setupUi(dialog, msg)
    dialog.ui.btnOk.clicked.connect(lambda: closeWindow(dialog))
    dialog.exec_()
    
    # Refresh list

    
    # We close the window
    self.close()
    
    
def closeWindow(window):
    window.close()