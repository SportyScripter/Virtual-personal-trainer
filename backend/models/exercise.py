from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base
from sqlalchemy import UniqueConstraint
import models


class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    body_part_id = Column(Integer, ForeignKey("body_parts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    exercise_name = Column(String, index=True)
    description = Column(String, nullable=True)

    exercise_videos = relationship("ExerciseVideo", back_populates="exercise")
    body_part = relationship("BodyPart", back_populates="exercise")
    user = relationship("User", back_populates="exercises")

    __table_args__ = (
        UniqueConstraint("user_id", "exercise_name", name="uq_user_exercise_name"),
    )

    class Config:
        orm_mode = True
