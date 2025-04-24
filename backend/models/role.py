from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base
import datetime
import models


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_name = Column(String, unique=True, index=True, default="user")
    description = Column(String)
    create_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )

    user = relationship("User", back_populates="role")

    class Config:
        orm_mode = True
