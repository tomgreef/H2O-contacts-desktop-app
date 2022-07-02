from bson import ObjectId
from itertools import imap
import controllers


class ClientModel(dict):
    """
    A simple ClientModel that wraps mongodb document
    """
    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    def save(self):
        if not self._id:
            self.collection.insert(self)
        else:
            self.collection.update(
                { "_id": ObjectId(self._id) }, self)

    def reload(self):
        if self._id:
            self.update(self.collection\
                    .find_one({"_id": ObjectId(self._id)}))

    def remove(self):
        if self._id:
            self.collection.remove({"_id": ObjectId(self._id)})
            self.clear()


# ------------------------------
# Here is the example ClientModel
# ------------------------------

class Document(ClientModel):
    
    collection = controllers.singleton.getInstance().clients

    @property
    def keywords(self):
        return self.title.split()


# ------------------------------
# Mapping documents to the ClientModel
# ------------------------------

documents = imap(Document, Document.collection.find())