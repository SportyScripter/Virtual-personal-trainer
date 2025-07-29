from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.base_class import Base
import datetime
import models


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role = Column(Integer, ForeignKey("roles.id"), default=1)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=1)  # 1 for active, 0 for inactive
    create_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )

    role = relationship("Role", back_populates="user")
    tokens = relationship("Token", back_populates="user")
    exercise_videos = relationship("ExerciseVideo", back_populates="user")
    exercises = relationship("Exercise", back_populates="user")

    class Config:
        orm_mode = True
