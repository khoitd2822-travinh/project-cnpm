from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from src.infrastructure.databases.base import Base

class assignmentModel(Base):
    __tablename__ = 'assignment'
    __table_args__ = {'extend_existing': True}

    assignment_id = Column(Integer, primary_key=True)
    paper_id = Column(Integer, ForeignKey('paper.paper_id'))
    reviewer_id = Column(Integer, ForeignKey('users.user_id'))
    assign_at = Column(DateTime)
    coi_declared = Column(Boolean)
