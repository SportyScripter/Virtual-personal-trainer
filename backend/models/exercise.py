from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base


class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    exercise_name = Column(String, unique=True, index=True)
    body_part = Column(String, ForeignKey("body_parts.body_part_name"))

    exercise_videos = relationship("ExerciseVideo", back_populates="exercise")
    body_part = relationship("BodyPart", back_populates="exercise")

    class Config:
        orm_mode = True
