from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.databases.base import Base

class usersmodel(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime)
