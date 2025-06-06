from db.session import get_db
from schemas.body_part import BodyPartCreate
from sqlalchemy.orm import Session
from models.body_part import BodyPart
from enum import Enum


class BodyPartEnum(Enum):
    CHEST = "Klatka piersiowa"
    BACK = "Plecy"
    THIGHS = "Uda"
    CALVES = "Łydki"
    BICEPS = "Biceps"
    TRICEPS = "Triceps"
    FOREARMS = "Przedramiona"
    SHOULDERS = "Barki"
    ABS = "Brzuch"
    GLUTES = "Pośladki"


def seed_body_parts(db: Session):
    for part in BodyPartEnum:
        exists = db.query(BodyPart).filter_by(body_part_name=part.value).first()
        if not exists:
            db.add(BodyPart(body_part_name=part.value))
            print(f"Added body part: {part.value}")
    db.commit()
