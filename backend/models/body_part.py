from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base
import models


class BodyPart(Base):
    __tablename__ = "body_parts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    body_part_name = Column(String, unique=True, index=True)
    body_part_description = Column(String)

    exercise = relationship("Exercise", back_populates="body_part")

    class Config:
        orm_mode = True
