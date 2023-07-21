from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship

from ..sql_app.database import Base


class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    terms = relationship("Term", back_populates="set")

    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="sets")