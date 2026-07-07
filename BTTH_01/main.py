from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Depends, Request, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from service import (create_parking_slot, get_all_parking_slots, get_parking_slot)

import models

app = FastAPI()

Base.metadata.create_all(bind=engine)


class ParkingSlotCreate(BaseModel):
    slot_code: str = Field(min_length=1)
    zone_name: str = Field(min_length=3)
    max_weight: int = Field( gt=0)
    is_available: Optional[bool] = True


def create_response(
    statusCode,
    message,
    error,
    data,
    path
):
    return {
        "statusCode": statusCode,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/parking-slots", status_code=201)
def add_parking_slot(
    parking_slot: ParkingSlotCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    result = create_parking_slot(parking_slot, db)

    return create_response(
        201,
        "Thêm vị trí đỗ xe thành công",
        None,
        {
            "id": result.id,
            "slot_code": result.slot_code,
            "zone_name": result.zone_name,
            "max_weight": result.max_weight,
            "is_available": result.is_available
        },
        request.url.path
    )


@app.get("/parking-slots")
def get_all(
    request: Request,
    db: Session = Depends(get_db)
):
    result = get_all_parking_slots(db)

    data = []

    for item in result:
        data.append({
            "id": item.id,
            "slot_code": item.slot_code,
            "zone_name": item.zone_name,
            "max_weight": item.max_weight,
            "is_available": item.is_available
        })

    return create_response(
        200,
        "Lấy danh sách vị trí đỗ xe thành công",
        None,
        data,
        request.url.path
    )


@app.get("/parking-slots/{slot_id}")
def get_one(
    slot_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        result = get_parking_slot(slot_id, db)

        return create_response(
            200,
            "Lấy chi tiết vị trí đỗ xe thành công",
            None,
            {
                "id": result.id,
                "slot_code": result.slot_code,
                "zone_name": result.zone_name,
                "max_weight": result.max_weight,
                "is_available": result.is_available
            },
            request.url.path
        )

    except HTTPException as e:
        return create_response(
            e.status_code,
            e.detail,
            "Not Found",
            None,
            request.url.path
        )
