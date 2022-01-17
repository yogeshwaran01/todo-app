import os.path
import json


class Database:
    def __init__(self, path) -> None:
        self.path = path
        if self.__is_database_exists():
            with open(path) as file:
                self.data = json.load(file)
        else:
            self.data = {}

    def __is_database_exists(self):
        return os.path.exists(self.path)

    def all_documents(self):
        return list(self.data.values())

    def __create_id(self):
        return str(len(self.data) + 1)

    def add_document(self, document):
        id_ = self.__create_id()
        document = {'id': id_} | document
        self.data[id_] = document
        return id_

    def get_document_by_id(self, id):
        return self.data.get(id)

    def delete_document_by_id(self, id):
        del self.data[id]

    def commit(self):
        with open(self.path, "w") as file:
            json.dump(self.data, file)
        return True
