from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint
from infrastructure.databases.base import Base


class usersmodel(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False) 
    created_at = Column(DateTime)

class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False) 

class UserConferenceRole(Base):
    __tablename__ = 'user_conference_roles'
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    conf_id = Column(Integer, ForeignKey('conference.conf_id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)
    
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'conf_id', 'role_id'),
        {'extend_existing': True}
    )