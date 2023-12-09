from abc import ABC, abstractmethod

class Function(ABC):
    @abstractmethod
    def execute(self, env):
        pass

    @abstractmethod
    def ast(self, ast):
        pass