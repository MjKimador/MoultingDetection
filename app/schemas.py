from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
from typing import List
from app.models import MoultingLog

class MoultingStage(str, Enum):
    not_started = "not started"
    moulting = "moulting"
    done = "done"

class PenguinBase(BaseModel):
    rfid_tag: str
    name: Optional[str]
    mass: float
    status: MoultingStage

class PenguinCreate(PenguinBase):
    pass

class PenguinOut(PenguinBase):
    id: int
    last_seen: datetime
    danger_flag: bool

    class Config:
        from_attributes = True


class MoultingLogCreate(BaseModel):
    penguin_id: int
    stage: str
    mass: float
    image_url: Optional[str] = None


class MoultingLogOut(BaseModel):
    id: int
    date: datetime
    stage: str
    mass: float

    class Config:
        from_attributes = True


class PenguinOutWithLogs(BaseModel):
    id: int
    name: str
    status: str
    mass: float
    danger_flag: bool
    created_at: datetime
    logs: List[MoultingLogOut]  # 🐧 Include logs

    class Config:
        from_attributes = True


