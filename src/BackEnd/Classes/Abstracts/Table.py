from abc import ABC, abstractmethod

class Table(ABC):
    @abstractmethod
    def insert(self, env, fields, line, column):
        pass

    @abstractmethod
    def validate(self, env, fields, line, column):
        pass

    @abstractmethod
    def validateFields(self, names):
        pass

    @abstractmethod
    def truncate(self):
        pass

    @abstractmethod
    def addColumn(self, newColumn, type):
        pass

    @abstractmethod
    def dropColumn(self, column):
        pass

    @abstractmethod
    def renameTo(self, newId):
        pass

    @abstractmethod
    def renameColumn(self, currentColumn, newColumn):
        pass

    @abstractmethod
    def createTmpFields(self):
        pass

    @abstractmethod
    def deleteWhere(self, condition, env):
        pass

    @abstractmethod
    def updateWhere(self, condition, fields, values, env):
        pass

    @abstractmethod
    def getAllFieldsTitle(self):
        pass

    @abstractmethod
    def getTitles(self, fieldsTitle):
        pass

    @abstractmethod
    def createSelectFields(self, titles):
        pass

    @abstractmethod
    def select(self, fields, condition, env):
        pass

    @abstractmethod
    def getTable(self, fields, rows):
        pass

    @abstractmethod
    def getFieldsRow(self):
        pass