from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from infrastructure.databases.base import Base

class reviewModel(Base):
    __tablename__ = 'review'
    __table_args__ = {'extend_existing': True}

    review_id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignment.assignment_id'))
    decision = Column(String(50))
    comments = Column(Text)
    decide_by = Column(Integer, ForeignKey('users.user_id'))
    decide_at = Column(DateTime)
