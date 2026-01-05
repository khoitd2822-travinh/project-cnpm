from flask import Blueprint, request, jsonify

from application.use_cases.assign_paper_use_case import AssignPaperUseCase
from src.infrastructure.repositories.paper_repository_impl import PaperRepository
from src.infrastructure.repositories.reviewer_repository_impl import ReviewerRepository

paper_bp = Blueprint("paper", __name__)

@paper_bp.route("/papers/assign", methods=["POST"])
def assign_paper():
    data = request.get_json()

    use_case = AssignPaperUseCase(
        PaperRepository(),
        ReviewerRepository()
    )

    result = use_case.execute(
        paper_id=data.get("paper_id"),
        reviewer_ids=data.get("reviewer_ids", [])
    )

    return jsonify(result)
