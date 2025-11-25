from datetime import datetime
from typing import Any

from pydantic import BaseModel, computed_field

from src.config import COFFEE_SETTINGS
from src.drink.step import BaseStep
from src.enums import TempType, CupType


class Drink(BaseModel):
    id: int
    full_name: str
    name: str
    capacity: int
    cup_type: CupType
    updated: datetime

    steps: list[BaseStep]

    enable: bool = True
    best_sell: bool = False
    save_out: bool = False
    is_checked: bool = True
    make_time: int = 70

    @computed_field
    def pic_path(self) -> str:
        return f"{self.name.replace(' ', '_')}_{self.capacity}"

    @computed_field
    def recipe_name(self) -> str:
        return f"{self.name} {self.capacity}"

    @computed_field
    def canister_ids_str(self) -> str:
        return ",".join([str(item.canister_id) for item in self.steps])

    @computed_field
    def drink_temp_type(self) -> TempType:
        for item in self.steps:
            temp_type = getattr(item, "temp_type", TempType.HOT)
            if temp_type and temp_type is TempType.COLD:
                return TempType.COLD
        return TempType.HOT

    @computed_field
    def es_attr(self) -> dict[str, Any] | None:
        for item in self.steps:
            if item.canister_id == 170:
                return COFFEE_SETTINGS
