from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from views.ui_clientForm import Ui_ClientForm
from views.ui_mainWindow import Ui_MainWindow
from views.ui_confirmationDialog import Ui_ConfirmationDialog
from PyQt5.QtWidgets import QDialog
from bson.objectid import ObjectId
from controllers.singleton import MongoManager
import sys, events


class clientForm(QMainWindow):

    def __init__(self):
        super(clientForm, self).__init__()
        self.ui = Ui_ClientForm()
        self.ui.setupUi(self)

        # --- Checkbox ---
        self.ui.water_only.clicked.connect(lambda: events.waterOnlyCheck(self.ui.water_only, self.ui.rental_price, self.ui.machine_type, self.ui.machines_in_pos))
        self.ui.account.clicked.connect(lambda: events.accountCheck(self.ui))

        # --- Events ---
        self.ui.btnRegister.clicked.connect(lambda: events.createClient(self))

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # --- Function ---
        self.createTable()
        
        # --- Events ---
        self.ui.btnAdd.clicked.connect(lambda: createAddWindow())   

        
    def createTable(self):
        # --- Load Clients ---
        # Create connection to DB
        db = MongoManager.getInstance()
        
        # List clients
        collection = db.clients
        cursor = collection.find()

        self.ui.table.setRowCount(0)
        self.ui.table.setColumnCount(0)
        
        for row_number, row_data in enumerate(cursor):
            self.ui.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if row_number == 0:
                    self.ui.table.insertColumn(column_number)
                    header = QTableWidgetItem(str(data).capitalize().replace('_', " "))
                    self.ui.table.setHorizontalHeaderItem(column_number, header)
                    
                item = QTableWidgetItem(str(row_data[data]))
                self.ui.table.setItem(row_number, column_number, item)

    
def createAddWindow():
    window = clientForm()
    window.show()

if __name__ == "__main__":
    # Initialize App
    app = QApplication(sys.argv)
    my_app = mainWindow()

    # Show UI
    my_app.show()
    sys.exit(app.exec_())