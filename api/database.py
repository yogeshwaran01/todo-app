import json
import os.path


class Database:
    """Handle json file crud operation"""

    def __init__(self, path: str) -> None:
        self.path = path
        if self.__is_database_exists():
            with open(path) as file:
                self.data = json.load(file)
        else:
            self.data = {}

    def __is_database_exists(self) -> bool:
        """Checks weather file is exists"""
        return os.path.exists(self.path)

    def all_documents(self) -> list:
        """Return all the documents"""
        return list(self.data.values())

    def __create_id(self) -> str:
        """Create unique id for each document"""
        return str(len(self.data) + 1)

    def add_document(self, document: dict) -> str:
        """Add a new document"""
        id_ = self.__create_id()
        document = {"id": id_} | document
        self.data[id_] = document
        return id_

    def get_document_by_id(self, id: str) -> dict:
        """Return the document of given id"""
        return self.data.get(id)

    def delete_document_by_id(self, id: str) -> None:
        """Delete the document of given id"""
        del self.data[id]

    def commit(self) -> bool:
        """Commit all changes to database"""
        with open(self.path, "w") as file:
            json.dump(self.data, file)
        return True
