from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from src.infrastructure.databases.base import Base

class auditlogModel(Base):
    __tablename__ = 'auditlogs'
    __table_args__ = {'extend_existing': True}

    log_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    action = Column(String(100))
    details = Column(Text)
    timestamp = Column(DateTime)
