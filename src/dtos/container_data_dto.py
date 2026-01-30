from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseContainerDataDTO:
    id: int
    name: str
    material_id: int


@dataclass(frozen=True, slots=True, kw_only=True)
class WaterContainerDataDTO(BaseContainerDataDTO):
    pass


@dataclass(frozen=True, slots=True, kw_only=True)
class CoffeeContainerDataDTO(BaseContainerDataDTO):
    total_product_quantity: float
    calibration_time: int
    discharge_speed: int


@dataclass(frozen=True, slots=True, kw_only=True)
class ContainerDataDTO(BaseContainerDataDTO):
    total_product_quantity: float
    discharge_speed: int
    calibration_time: int
