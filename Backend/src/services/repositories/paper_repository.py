from abc import ABC, abstractmethod

class IPaperRepository(ABC):
    @abstractmethod
    def get_by_id(self, paper_id):
        pass

    @abstractmethod
    def save(self, paper):
        pass
