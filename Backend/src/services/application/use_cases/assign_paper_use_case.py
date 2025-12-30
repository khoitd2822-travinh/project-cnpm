class AssignPaperUseCase:
    def __init__(self, paper_repo, reviewer_repo):
        self.paper_repo = paper_repo
        self.reviewer_repo = reviewer_repo

    def execute(self, paper_id, reviewer_ids):
        if not paper_id or not reviewer_ids:
            return {"success": False, "message": "Invalid input"}

        paper = self.paper_repo.get_by_id(paper_id)
        if not paper:
            return {"success": False, "message": "Paper not found"}

        reviewers = self.reviewer_repo.get_by_ids(reviewer_ids)
        if len(reviewers) != len(reviewer_ids):
            return {"success": False, "message": "Invalid reviewer list"}

        paper.assign_reviewers(reviewer_ids)
        self.paper_repo.save(paper)

        return {"success": True, "message": "Paper assigned successfully"}
