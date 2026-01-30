from typing import Annotated

from pydantic import BaseModel, BeforeValidator

from src.domain.enums import CupType


class StepModel(BaseModel):
    name: Annotated[str, BeforeValidator(lambda val: val.strip())]
    component_weight: Annotated[int | None, BeforeValidator(lambda val: val or None)]
    water_volume: int


class DrinkModel(BaseModel):
    id: int
    is_active: bool
    name: Annotated[str, BeforeValidator(lambda val: val.strip())]
    capacity: int
    price: int
    steps: list[StepModel]

    cup_type: Annotated[CupType | None, BeforeValidator(lambda val: val or None)]
