from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, BeforeValidator

from src.enums import CupType


class StepModel(BaseModel):
    name: str
    component_weight: int
    water_volume: int


class DrinkModel(BaseModel):
    id: int
    name: str
    capacity: int
    steps: list[StepModel]
    updated: Annotated[datetime, BeforeValidator(lambda val: datetime.strptime(val, "%d.%m.%Y %H:%M:%S"))]

    cup_type: Annotated[CupType | None, BeforeValidator(lambda val: val or None)]


class ProductModel(BaseModel):
    drink_id: int
    matrix_id: int
    price: int
    visible: bool
