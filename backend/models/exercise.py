from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base
import models


class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    exercise_name = Column(String, unique=True, index=True)
    body_part_id = Column(Integer, ForeignKey("body_parts.id"))
    description = Column(String, nullable=True)
    
    exercise_videos = relationship("ExerciseVideo", back_populates="exercise")
    body_part = relationship("BodyPart", back_populates="exercise")

    class Config:
        orm_mode = True
