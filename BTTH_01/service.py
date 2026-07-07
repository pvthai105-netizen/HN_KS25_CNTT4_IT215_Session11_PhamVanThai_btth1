from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models import ParkingSlot


def create_parking_slot(data, db: Session):
    try:
        parking_slot = ParkingSlot(
            slot_code=data.slot_code,
            zone_name=data.zone_name,
            max_weight=data.max_weight,
            is_available=data.is_available
        )

        db.add(parking_slot)
        db.commit()
        db.refresh(parking_slot)

        return parking_slot

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot code already exists"
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Error"
        )


def get_all_parking_slots(db: Session):
    return db.query(ParkingSlot).all()


def get_parking_slot(slot_id: int, db: Session):
    parking_slot = db.query(ParkingSlot).filter(
        ParkingSlot.id == slot_id
    ).first()

    if not parking_slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking slot not found"
        )

    return parking_slot
