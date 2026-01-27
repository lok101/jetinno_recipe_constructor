from pydantic import BaseModel

from src.config import DEFAULT_MIX_SPEED
from src.enums import TempType, IntensityVariable, DischargeSpeed, MixSpeed


class BaseStep(BaseModel):
    name: str
    order: int
    water_volume: int
    canister_id: int

    is_intensity_variable: IntensityVariable = IntensityVariable.DISABLE

    delay_time: int = 0
    add_recipe_time: int = 0


class WaterStep(BaseStep):
    name: str = "Вода"
    canister_id: int = 0
    component_weight: None


class CoffeeStep(BaseStep):
    name: str = "Кофе"
    canister_id: int = 170
    component_weight: int


class PowderStep(BaseStep):
    component_weight: int
    mix_speed: MixSpeed = DEFAULT_MIX_SPEED
    discharge_speed: DischargeSpeed

    temp_type: TempType = TempType.HOT
    # is_intensity_variable: IntensityVariable = IntensityVariable.DISABLE


class ColdPowderStep(PowderStep):
    temp_type: TempType = TempType.COLD

class SugarStep(PowderStep):
    is_intensity_variable: IntensityVariable = IntensityVariable.ENABLE
