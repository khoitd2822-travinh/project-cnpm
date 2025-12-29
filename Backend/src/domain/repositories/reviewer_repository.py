from abc import ABC, abstractmethod

class IReviewerRepository(ABC):
    @abstractmethod
    def get_by_ids(self, reviewer_ids):
        pass
