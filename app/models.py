from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import enum
from datetime import datetime
from datetime import datetime
from sqlalchemy.sql import func



class MoultingStage(str, enum.Enum):
    not_started = "not started"
    moulting = "moulting"
    done = "done"

class Penguin(Base):
    __tablename__ = "penguins"
    id = Column(Integer, primary_key=True, index=True)
    rfid_tag = Column(String(50), unique=True, nullable=False)
    name = Column(String(50))
    mass = Column(Float)
    last_seen = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(MoultingStage), default=MoultingStage.not_started)
    danger_flag = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    moulting_logs = relationship("MoultingLog", back_populates="penguin")
    images = relationship("PenguinImage", backref="penguin")

class MoultingLog(Base):
    __tablename__ = "moulting_logs"
    id = Column(Integer, primary_key=True, index=True)
    penguin_id = Column(Integer, ForeignKey("penguins.id"))
    date = Column(DateTime, default=func.now())
    stage = Column(Enum(MoultingStage))
    #image_url = Column(String(255), nullable=True)  # or image_path if local
    penguin = relationship("Penguin", back_populates="moulting_logs")
class PenguinImage(Base):
    __tablename__ = "penguin_images"

    id = Column(Integer, primary_key=True, index=True)
    penguin_id = Column(Integer, ForeignKey("penguins.id"))
    image_path = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
