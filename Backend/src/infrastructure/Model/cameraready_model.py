from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from infrastructure.databases.base import Base

class camerareadyModel(Base):
    __tablename__ = 'camera_ready'
    __table_args__ = {'extend_existing': True}

    cr_id = Column(Integer, primary_key=True)
    paper_id = Column(Integer, ForeignKey('paper.paper_id'))
    file_path = Column(String(255))
    upload_at = Column(DateTime)
