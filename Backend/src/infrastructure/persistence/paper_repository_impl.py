from Backend.src.domain.entities.paper import Paper
from src.domain.repositories.paper_repository import IPaperRepository

_FAKE_PAPERS = {
    1: Paper(1, "AI Conference Paper")
}

class PaperRepository(IPaperRepository):
    def get_by_id(self, paper_id):
        return _FAKE_PAPERS.get(paper_id)

    def save(self, paper):
        _FAKE_PAPERS[paper.paper_id] = paper
