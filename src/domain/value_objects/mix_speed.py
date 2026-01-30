from dataclasses import dataclass

from src.domain.enums import DischargeSpeedStepNumber


@dataclass(frozen=True, slots=True)
class MixSpeed:
    speed: DischargeSpeedStepNumber
    quantity: float
