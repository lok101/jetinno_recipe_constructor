import re
from dataclasses import dataclass

from src.domain.entities.step import BaseStep
from src.domain.enums import CupType, StepTempType, DrinkTempType


@dataclass(frozen=True, slots=True)
class MachineDrink:
    id: int
    name: str
    order: int
    price: int
    capacity: int
    cup_type: CupType
    recipe_name: str
    steps: list[BaseStep]

    def get_pic_path(self) -> str:
        return f"{self.id}.png"

    def get_recipe_name(self) -> str:
        return f"{self.name} {self.capacity}"

    def get_canister_ids_str(self) -> str:
        return ",".join([str(item.canister_id) for item in self.steps])

    def get_drink_temp_type(self) -> DrinkTempType:
        for item in self.steps:
            temp_type = getattr(item, "temp_type", StepTempType.HOT)
            if temp_type and temp_type is StepTempType.COLD:
                return DrinkTempType.COLD
        return DrinkTempType.HOT
