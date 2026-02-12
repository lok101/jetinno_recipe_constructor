import os
from typing import Annotated

from pydantic import BaseModel, Field, field_serializer

from domain.enums import ComponentName
from src.domain.entities.vending_machine_profile import VendingMachineProfile
from src.dtos.container_data_dto import BaseContainerDataDTO


class CanisterConfigModel(BaseModel):
    id: Annotated[int, Field(serialization_alias="canister_id")]
    name: Annotated[str, Field(serialization_alias="canister_name")]

    total_product_quantity: Annotated[float, Field(serialization_alias="test_results", default=None)]

    @field_serializer("total_product_quantity")
    def serialize_total_product_quantity(self, value: float | None) -> float | None:
        return round(value, 1) if value is not None else value

    discharge_speed: Annotated[int, Field(serialization_alias="dischargSpeed", default=None)]
    calibration_time: Annotated[int, Field(serialization_alias="time", default=None)]

    is_remain_minus: Annotated[bool, Field(serialization_alias="isRemainMinus", default=False)]
    material_id: int

    concentration_level: Annotated[int, Field(serialization_alias="concentrationLevel", default=0)]
    concentration_scale: Annotated[int, Field(serialization_alias="concentrationScale", default=0)]
    enable_zero_level: Annotated[int, Field(serialization_alias="enableZeroLevel", default=-1)]

    is_showed: Annotated[int, Field(default=0)]
    lack_remain: Annotated[int, Field(serialization_alias="lackRemain", default=50)]
    max_value: Annotated[int, Field(serialization_alias="maxValue", default=999)]


class CanistersData(BaseModel):
    data: list[CanisterConfigModel]


class SaveContainersConfigurationAdapter:
    def save_to_json(self, machine_profile: VendingMachineProfile, used_component_names: set[ComponentName]):
        containers_data: list[BaseContainerDataDTO] = machine_profile.get_containers_parameters()

        # Фильтруем только используемые контейнеры
        filtered_containers = [
            container for container in containers_data
            if container.name in used_component_names
        ]

        canisters_data = CanistersData.model_validate({"data": filtered_containers}, from_attributes=True)

        self._save_to_file(canisters_data)

    @staticmethod
    def _save_to_file(canisters_data: CanistersData):
        os.makedirs("Jetinno/Config", exist_ok=True)
        with open(f'Jetinno/Config/canister_config.json', 'wb') as file:
            json_data = canisters_data.model_dump_json(by_alias=True, exclude_none=True)
            bytes_data = json_data.encode('utf-8')
            file.write(bytes_data)
