from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..sql_app.database import Base

from sqlalchemy.orm import relationship

class Setting(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)

    options = relationship("Level", back_populates="setting")
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="settings")

class Level(Base):
    __tablename__ = "levels"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)
    is_selected = Column(Boolean)

    setting_id = Column(Integer, ForeignKey("settings.id"))
    setting = relationship("Setting", back_populates="options")
