from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from infrastructure.databases.base import Base

class decisionModel(Base):
    __tablename__ = 'decision'
    __table_args__ = {'extend_existing': True}

    decision_id = Column(Integer, primary_key=True)
    paper_id = Column(Integer, ForeignKey('paper.paper_id'))
    decision = Column(String(50))
    decide_by = Column(Integer, ForeignKey('users.user_id'))
    decide_at = Column(DateTime)
