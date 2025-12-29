from infrastructure.databases.postgresql import init_postgresql
from infrastructure.Model import users_model, paper_model, assignment_model, audilog_model, cameraready_model, conference_model, review_model, track_model

def init_db(app):
    init_postgresql(app)
    
