from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

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
        orm_mode = True

class MoultingLogCreate(BaseModel):
    penguin_id: int
    stage: MoultingStage

class MoultingLogOut(BaseModel):
    id: int
    penguin_id: int
    date: datetime
    stage: MoultingStage

    class Config:
        from_attributes = True  # Replace orm_mode for Pydantic V2

