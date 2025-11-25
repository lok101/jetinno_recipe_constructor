from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, BeforeValidator

from src.enums import CupType


class StepModel(BaseModel):
    name: Annotated[str, BeforeValidator(lambda val: val.strip())]
    component_weight: Annotated[int | None, BeforeValidator(lambda val: val or None)]
    water_volume: int


class DrinkModel(BaseModel):
    id: int
    full_name: str
    name: Annotated[str, BeforeValidator(lambda val: val.strip())]
    capacity: int
    steps: list[StepModel]
    updated: Annotated[datetime, BeforeValidator(lambda val: datetime.strptime(val, "%d.%m.%Y %H:%M:%S"))]

    cup_type: Annotated[CupType | None, BeforeValidator(lambda val: val or None)]


class ProductModel(BaseModel):
    full_name: str
    matrix_id: int
    price: int
    visible: Annotated[bool, BeforeValidator(lambda val: bool(val))]
