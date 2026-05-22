import abc

class Observer(abc.ABC):
    """Интерфейс Наблюдателя."""
    @abc.abstractmethod
    def update(self, message: str):
        pass

class Subject(abc.ABC):
    """Интерфейс Издателя."""
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

class CombatLog(Observer):
    """Конкретный Наблюдатель: Боевой лог."""
    def __init__(self, max_lines=100):
        self.logs = []
        self.max_lines = max_lines

    def update(self, message: str):
        self.logs.append(message)
        if len(self.logs) > self.max_lines:
            self.logs.pop(0)
            
    def get_logs(self):
        return self.logs
