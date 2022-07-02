 def updateClient(self, item):
        db = singleton.MongoManager.getInstance()
        collection = db.clients
         
        row = item.row()
        col = item.column()
        
        if col == 0 :
            dialog = QDialog()
            dialog.ui = Ui_ConfirmationDialog()
            msg = "You can't change the ID"
            dialog.ui.setupUi(dialog, msg)
            dialog.ui.btnOk.clicked.connect(lambda: events.closeWindow(dialog))
            dialog.exec_()
        else:
            id = ObjectId(str(self.ui.table.item(row, 0).text()))
            column = str(self.ui.table.horizontalHeaderItem(col).text()).lower()

            myQuery = { "_id": id }
            newValues = { "$set": { column : str(item.text()) } }
            result = collection.update_one(myQuery, newValues)