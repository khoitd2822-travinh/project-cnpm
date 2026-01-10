from src.domain.entities.reviewer import Reviewer
from src.domain.repositories.reviewer_repository import IReviewerRepository

_FAKE_REVIEWERS = {
    1: Reviewer(1, "Reviewer A"),
    2: Reviewer(2, "Reviewer B")
}

class ReviewerRepository(IReviewerRepository):
    def get_by_ids(self, reviewer_ids):
        return [r for i, r in _FAKE_REVIEWERS.items() if i in reviewer_ids]
