from sqlalchemy.orm import Session

from . import models, schemas
from datetime import datetime
from collections import Counter
from sqlalchemy import func
from app.models import Penguin
from sqlalchemy import or_, and_
from datetime import datetime, timedelta, timezone
from app.models import Penguin, MoultingLog
from typing import Optional


def create_penguin(db: Session, penguin: schemas.PenguinCreate):
    db_penguin = models.Penguin(**penguin.dict(), last_seen=datetime.now(timezone.utc))
    db.add(db_penguin)
    db.commit()
    db.refresh(db_penguin)
    return db_penguin

def get_penguins(db: Session):
    return db.query(models.Penguin).all()

def get_penguin(db: Session, penguin_id: int):
    return db.query(models.Penguin).filter(models.Penguin.id == penguin_id).first()
def create_moulting_log(db: Session, log: schemas.MoultingLogCreate):
    moulting_log = MoultingLog(
        penguin_id=log.penguin_id,
        stage=log.stage,
        mass=log.mass,
        image_url=log.image_url
    )
    db.add(moulting_log)
    db.commit()
    db.refresh(moulting_log)
    # After adding the moulting log entry
    penguin = db.query(models.Penguin).filter(models.Penguin.id == log.penguin_id).first()
    if penguin:
        penguin.status = log.stage
        penguin.mass = log.mass
        penguin.last_seen = moulting_log.date  # ✅ Use actual saved log date

    db.commit()
    return moulting_log


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
    total_penguins = db.query(models.Penguin).count()

    if total_penguins == 0:
        return {
            "total_penguins": 0,
            "moulting_stages": {},
            "average_mass": None,
            "stddev_mass": None,
            "min_mass": None,
            "max_mass": None,
            "at_risk_count": 0,
            "at_risk_percentage": "0%",
            "never_logged_count": 0,
            "average_hours_since_seen": None,
            "latest_seen": None
        }

    # Moulting stage breakdown
    moulting_counts = (
        db.query(models.Penguin.status, func.count(models.Penguin.id))
        .group_by(models.Penguin.status)
        .all()
    )
    moulting_stages = {stage: count for stage, count in moulting_counts}

    # Mass stats
    stats = db.query(
        func.avg(models.Penguin.mass),
        func.stddev_pop(models.Penguin.mass),
        func.min(models.Penguin.mass),
        func.max(models.Penguin.mass)
    ).first()
    avg_mass, std_mass, min_mass, max_mass = stats

    # Risky penguins
    at_risk_count = db.query(models.Penguin).filter(models.Penguin.danger_flag == True).count()
    at_risk_percentage = f"{(at_risk_count / total_penguins * 100):.2f}%" if total_penguins else "0%"

    # Never logged penguins
    never_logged_count = (
        db.query(models.Penguin)
        .filter(~models.Penguin.logs.any())
        .count()
    )

    # Average hours since last seen
    now = datetime.utcnow()
    last_seen_times = (
        db.query(models.MoultingLog.penguin_id, func.max(models.MoultingLog.date))
        .group_by(models.MoultingLog.penguin_id)
        .all()
    )
    if last_seen_times:
        avg_hours = sum([(now - log_time).total_seconds() / 3600 for _, log_time in last_seen_times]) / len(last_seen_times)
    else:
        avg_hours = None

    # Latest seen penguin
    latest_seen_log = (
        db.query(models.MoultingLog)
        .order_by(models.MoultingLog.date.desc())
        .first()
    )
    latest_seen = {
        "penguin_id": latest_seen_log.penguin_id,
        "last_seen": latest_seen_log.date
    } if latest_seen_log else None

    return {
        "total_penguins": total_penguins,
        "moulting_stages": moulting_stages,
        "average_mass": avg_mass,
        "stddev_mass": std_mass,
        "min_mass": min_mass,
        "max_mass": max_mass,
        "at_risk_count": at_risk_count,
        "at_risk_percentage": at_risk_percentage,
        "never_logged_count": never_logged_count,
        "average_hours_since_seen": avg_hours,
        "latest_seen": latest_seen
    }

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
def get_all_penguins_sorted(db: Session, sort_by: Optional[str] = None):
    base_query = db.query(Penguin)

    if sort_by == "weight":
        base_query = base_query.order_by(Penguin.mass.asc())

    elif sort_by == "risk":
        # True first, then False (dangerous → safe)
        base_query = base_query.order_by(Penguin.danger_flag.desc())

    elif sort_by == "last_seen":
        log_subquery = (
            db.query(
                MoultingLog.penguin_id.label("pid"),
                func.max(MoultingLog.date).label("last_seen")
            )
            .group_by(MoultingLog.penguin_id)
            .subquery()
        )

        # Use COALESCE to default to penguin.created_at if no logs
        result = (
            db.query(Penguin, func.coalesce(log_subquery.c.last_seen, Penguin.created_at).label("effective_last_seen"))
            .outerjoin(log_subquery, Penguin.id == log_subquery.c.pid)
            .order_by(func.coalesce(log_subquery.c.last_seen, Penguin.created_at).desc())
            .all()
        )

        return [row[0] for row in result]


    return base_query.all()

def search_penguins(db: Session, query: str):
    if query.isdigit():
        # Search by ID
        return db.query(Penguin).filter(Penguin.id == int(query)).all()
    else:
        # Search by partial name (case insensitive)
        return db.query(Penguin).filter(Penguin.name.ilike(f"%{query}%")).all()


