from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..sql_app.database import Base

from sqlalchemy.orm import relationship

class Term(Base):
    __tablename__ = "terms"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(String)
    positive_points = Column(Integer)
    negative_points = Column(Integer)
    set_id = Column(Integer, ForeignKey("sets.id"))
    set = relationship("Set", back_populates="terms")