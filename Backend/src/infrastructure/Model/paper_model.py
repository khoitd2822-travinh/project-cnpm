from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.infrastructure.databases.base import Base

class paperModel(Base):
    __tablename__ = 'paper'
    __table_args__ = {'extend_existing': True}

    paper_id = Column(Integer, primary_key=True)
    conf_id = Column(Integer, ForeignKey('conference.conf_id'))
    track_id = Column(Integer, ForeignKey('track.track_id'))
    title = Column(String(255), nullable=False)
    file_path = Column(String(255))
    status = Column(String(50))
    submitted_at = Column(DateTime)
    updated_at = Column(DateTime)
