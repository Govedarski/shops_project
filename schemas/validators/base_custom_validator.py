from abc import abstractmethod, ABC


class BaseCustomValidator(ABC):
    ERROR = ""

    @abstractmethod
    def validate(self, value):
        pass

    def _get_error_message(self, value):
        return self.ERROR
