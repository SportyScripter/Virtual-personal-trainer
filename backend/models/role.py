from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_name = Column(String, unique=True, index=True)
    description = Column(String)
    create_at = Column(DateTime)
    updated_at = Column(DateTime)

    user = relationship("User", back_populates="role")

    class Config:
        orm_mode = True
