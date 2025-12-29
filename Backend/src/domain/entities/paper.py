class Paper:
    def __init__(self, paper_id, title, assigned_reviewers=None):
        self.paper_id = paper_id
        self.title = title
        self.assigned_reviewers = assigned_reviewers or []

    def assign_reviewers(self, reviewer_ids):
        self.assigned_reviewers = reviewer_ids
