from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Paper, Conference, CameraReady, AuditLog
from werkzeug.utils import secure_filename
import os
from datetime import datetime

author_bp = Blueprint('author', __name__)

def log_audit(user_id, action, details=""):
    audit = AuditLog(
        user_id=user_id,
        action=action,
        details=details,
        timestamp=datetime.utcnow()
    )
    db.session.add(audit)
    db.session.commit()


@author_bp.route('/papers', methods=['POST'])
@jwt_required()
def submit_paper():
    user = get_jwt_identity()

    if user['role'] != 'author':
        return jsonify({"error": "Only authors can submit papers"}), 403

    title = request.form.get('title')
    conf_id = request.form.get('conf_id')
    file = request.files.get('file')

    if not title or not conf_id or not file:
        return jsonify({"error": "Missing data"}), 400

    conf = Conference.query.get(conf_id)
    if not conf:
        return jsonify({"error": "Conference not found"}), 404

    if datetime.utcnow() > conf.submission_deadline:
        return jsonify({"error": "Submission deadline passed"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    paper = Paper(
        title=title,
        conf_id=conf_id,
        user_id=user['user_id'],
        file_path=filepath,
        status='submitted'
    )
    db.session.add(paper)
    db.session.commit()

    log_audit(user['user_id'], 'submit_paper', f"Paper ID: {paper.paper_id}")

    return jsonify({"message": "Paper submitted", "paper_id": paper.paper_id}), 201


@author_bp.route('/papers/<int:paper_id>', methods=['PUT'])
@jwt_required()
def edit_paper(paper_id):
    user = get_jwt_identity()
    paper = Paper.query.get(paper_id)

    if not paper or paper.user_id != user['user_id']:
        return jsonify({"error": "Not the owner"}), 403

    conf = Conference.query.get(paper.conf_id)
    if datetime.utcnow() > conf.submission_deadline:
        return jsonify({"error": "Submission deadline passed"}), 400

    title = request.form.get('title', paper.title)
    file = request.files.get('file')

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        paper.file_path = filepath

    paper.title = title
    paper.updated_at = datetime.utcnow()
    db.session.commit()

    log_audit(user['user_id'], 'edit_paper', f"Paper ID: {paper_id}")

    return jsonify({"message": "Paper edited"})


@author_bp.route('/papers/<int:paper_id>/withdraw', methods=['DELETE'])
@jwt_required()
def withdraw_paper(paper_id):
    user = get_jwt_identity()
    paper = Paper.query.get(paper_id)

    if not paper or paper.user_id != user['user_id']:
        return jsonify({"error": "Not the owner"}), 403

    paper.status = 'withdrawn'
    db.session.commit()

    log_audit(user['user_id'], 'withdraw_paper', f"Paper ID: {paper_id}")

    return jsonify({"message": "Paper withdrawn"})


@author_bp.route('/papers/<int:paper_id>/camera-ready', methods=['POST'])
@jwt_required()
def upload_camera_ready(paper_id):
    user = get_jwt_identity()
    paper = Paper.query.get(paper_id)

    if not paper or paper.user_id != user['user_id'] or paper.status != 'accepted':
        return jsonify({"error": "Not allowed"}), 403

    file = request.files.get('file')
    if not file:
        return jsonify({"error": "File required"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    camera = CameraReady(
        paper_id=paper_id,
        file_path=filepath
    )
    db.session.add(camera)

    paper.status = 'camera_ready'
    db.session.commit()

    log_audit(user['user_id'], 'upload_camera_ready', f"Paper ID: {paper_id}")

    return jsonify({"message": "Camera-ready uploaded"})
