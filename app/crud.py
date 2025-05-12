from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from collections import Counter
from sqlalchemy import func
from app.models import Penguin
from sqlalchemy import or_, and_
from datetime import datetime, timedelta
from app.models import Penguin, MoultingLog

def create_penguin(db: Session, penguin: schemas.PenguinCreate):
    db_penguin = models.Penguin(**penguin.dict(), last_seen=datetime.utcnow())
    db.add(db_penguin)
    db.commit()
    db.refresh(db_penguin)
    return db_penguin

def get_penguins(db: Session):
    return db.query(models.Penguin).all()

def get_penguin(db: Session, penguin_id: int):
    return db.query(models.Penguin).filter(models.Penguin.id == penguin_id).first()
def create_moulting_log(db: Session, log: schemas.MoultingLogCreate):
    db_log = models.MoultingLog(**log.dict())
    db.add(db_log)

    # Update penguin's status
    penguin = db.query(models.Penguin).filter(models.Penguin.id == log.penguin_id).first()
    if penguin:
        penguin.status = log.stage
        penguin.last_seen = datetime.utcnow()

        # Risk logic: flag if moulting but underweight (< 2.5kg)
        if log.stage == models.MoultingStage.moulting and penguin.mass < 2.5:
            penguin.danger_flag = True
        else:
            penguin.danger_flag = False

    db.commit()
    db.refresh(db_log)
    return db_log

def get_moulting_logs_for_penguin(db: Session, penguin_id: int):
    return db.query(models.MoultingLog).filter(models.MoultingLog.penguin_id == penguin_id).all()

def get_risk_penguins(db: Session):
    penguins = db.query(models.Penguin).all()
    at_risk = []

    for p in penguins:
        if p.status == models.MoultingStage.moulting and p.mass < 2.5:
            p.danger_flag = True
            at_risk.append(p)
        else:
            p.danger_flag = False  # Keep it clean if they’re no longer at risk

    db.commit()
    return at_risk

def get_stage_counts(db: Session):
    penguins = db.query(models.Penguin).all()
    counts = Counter(p.status for p in penguins)
    return counts


def get_colony_stats(db: Session):
    stats = {
        "total_penguins": 0,
        "not started": 0,
        "moulting": 0,
        "done": 0
    }

    stats["total_penguins"] = db.query(func.count(Penguin.id)).scalar()

    result = (
        db.query(Penguin.status, func.count(Penguin.id))
        .group_by(Penguin.status)
        .all()
    )

    for stage, count in result:
        if stage in stats:
            stats[stage] = count

    return stats
# crud.py
def get_unlogged_penguins(db: Session):
    one_day_ago = datetime.utcnow() - timedelta(days=1)

    # Subquery to get latest log date per penguin
    subquery = (
        db.query(
            MoultingLog.penguin_id,
            func.max(MoultingLog.date).label("last_log_date")
        )
        .group_by(MoultingLog.penguin_id)
        .subquery()
    )

    # Join penguins with their latest log
    result = (
        db.query(Penguin, subquery.c.last_log_date)
        .outerjoin(subquery, Penguin.id == subquery.c.penguin_id)
        .filter(or_(
            subquery.c.last_log_date == None,
            subquery.c.last_log_date < one_day_ago
        ))
        .all()
    )

    return result

def delete_penguin(db: Session, penguin_id: int):
    penguin = db.query(Penguin).filter(Penguin.id == penguin_id).first()
    if not penguin:
        return None
    db.delete(penguin)
    db.commit()
    return penguin
