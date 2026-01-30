import math
from dataclasses import dataclass

from src.domain.exceptions import TooManyComponentWeight
from src.domain.value_objects.mix_speed import MixSpeed
from src.domain.enums import DischargeSpeed, ComponentName, material_ids, POWDER_MATERIAL_ID, COFFEE_CONTAINER_ID, \
    WATER_CONTAINER_ID
from src.dtos.container_data_dto import ContainerDataDTO, CoffeeContainerDataDTO, WaterContainerDataDTO


@dataclass(frozen=True, slots=True)
class Container:
    id: int
    component_name: ComponentName
    min_speed: MixSpeed
    max_speed: MixSpeed

    def get_discharge_speed(self, component_weight: int, water_volume: int, water_per_second: int) -> DischargeSpeed:
        speeds_list = list(DischargeSpeed)

        step_time = water_volume / water_per_second
        gr_per_second = component_weight / step_time

        if gr_per_second > self.max_speed.quantity:
            min_water = component_weight / self.max_speed.quantity * water_per_second

            raise TooManyComponentWeight(
                f"Требуемая скорость подачи порошка - выше максимальной.\n"
                f"max: {self.max_speed.quantity}\n"
                f"current: gr_per_second\n"
                f"component_name: {self.component_name}\n"
                f"component_weight: {component_weight}\n"
                f"water_volume: {water_volume}\n"
                f"min_water: {min_water}\n"
            )

        quantity_difference = self.max_speed.quantity - self.min_speed.quantity
        speed_numbers_difference = self.max_speed.speed.value - self.min_speed.speed.value

        linear_k = quantity_difference / speed_numbers_difference
        linear_b = self.max_speed.quantity - self.max_speed.speed.value * linear_k

        speed = (gr_per_second - linear_b) / linear_k

        speed_index = math.ceil(speed) - 1

        if speed_index < 0:
            raise Exception("Индекс скорости подачи порошка не должен быть отрицательным.")

        if speed_index > len(speeds_list) - 1:
            return speeds_list[-1]

        return speeds_list[speed_index]

    def as_container_data_dto(self, calibration_time: int) -> ContainerDataDTO:
        speeds = list(DischargeSpeed)

        discharge_speed: DischargeSpeed = speeds[self.max_speed.speed.value - 1]

        return ContainerDataDTO(
            id=self.id,
            name=self.component_name,
            calibration_time=calibration_time,
            total_product_quantity=self.max_speed.quantity * calibration_time,
            discharge_speed=discharge_speed,
            material_id=self._get_material_id(component_name=self.component_name)
        )

    @staticmethod
    def _get_material_id(component_name: ComponentName) -> int:
        return material_ids.get(component_name, POWDER_MATERIAL_ID)

    @classmethod
    def get_coffee_container(cls, calibration_time: int, calibration_value: float) -> CoffeeContainerDataDTO:
        return CoffeeContainerDataDTO(
            id=COFFEE_CONTAINER_ID,
            name=ComponentName.COFFEE,
            calibration_time=calibration_time,
            total_product_quantity=calibration_value * calibration_time,
            material_id=cls._get_material_id(component_name=ComponentName.COFFEE),
            discharge_speed=13
        )

    @classmethod
    def get_water_container(cls) -> WaterContainerDataDTO:
        return WaterContainerDataDTO(
            id=WATER_CONTAINER_ID,
            name=ComponentName.WATER,
            material_id=cls._get_material_id(component_name=ComponentName.WATER)
        )
