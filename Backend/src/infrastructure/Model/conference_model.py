from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from infrastructure.databases.base import Base

class conferenceModel(Base):
    __tablename__ = 'conference'
    __table_args__ = {'extend_existing': True}

    conf_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    submission_deadline = Column(DateTime)
    review_deadline = Column(DateTime)
    chair_id = Column(Integer, ForeignKey('users.user_id'))
