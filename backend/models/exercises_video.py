from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base
import datetime
import models


class ExerciseVideo(Base):
    __tablename__ = "exercise_videos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    video_path = Column(String)
    create_at = Column(DateTime, default=datetime.datetime.now)

    user = relationship("User", back_populates="exercise_videos")
    exercise = relationship("Exercise", back_populates="exercise_videos")

    class Config:
        orm_mode = True
