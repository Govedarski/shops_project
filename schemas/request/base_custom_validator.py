from abc import abstractmethod, ABC


class BaseCustomValidator(ABC):
    ERROR = ""

    @abstractmethod
    def validate(self, value):
        pass
