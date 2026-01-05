from sqlalchemy import Column, Integer, String, Text, ForeignKey
from src.infrastructure.databases.base import Base

class trackmodel(Base):
    __tablename__ = 'track'
    __table_args__ = {'extend_existing': True}

    track_id = Column(Integer, primary_key=True)
    conf_id = Column(Integer, ForeignKey('conference.conf_id'))
    name = Column(String(100), nullable=False)
    description = Column(Text)
