import json
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.domain.enums import ComponentName
from src.domain.entities.container import Container
from src.domain.entities.vending_machine_profile import VendingMachineProfile
from src.domain.enums import MachineModel, DischargeSpeedStepNumber
from src.domain.value_objects.mix_speed import MixSpeed


class DischargeSpeedItem(BaseModel):
    speed: int
    quantity: float


class ContainerData(BaseModel):
    id: int
    component_name: str
    min_speed: DischargeSpeedItem
    max_speed: DischargeSpeedItem


class VendingMachineSettings(BaseModel):
    model: str
    recipe_table_name: str
    water_per_second: int
    calibration_time: int
    coffee_per_second: float

    containers_data: list[Container]


class MachineProfilesSettings(BaseSettings):
    """Настройки аккаунтов Kit Vending."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="KIT_VENDING_",
        case_sensitive=False,
        extra="ignore",
    )

    profiles_file: Annotated[
        Path,
        Field(
            default=Path("kit_vending_accounts.json"),
            description="Путь к JSON файлу с аккаунтами",
        ),
    ] = Path("machine_profiles.json")

    profiles: list[VendingMachineSettings] = Field(default_factory=list)

    @field_validator("profiles_file", mode="before")
    @classmethod
    def validate_profiles_file(cls, v: str | Path) -> Path:
        """Преобразует строку в Path объект."""
        if isinstance(v, str):
            return Path(v)
        return v

    @model_validator(mode="after")
    def load_profiles_from_file(self) -> "MachineProfilesSettings":
        loaded_profiles: list[VendingMachineSettings] = []
        if self.profiles_file.exists():
            with open(self.profiles_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    loaded_profiles = [VendingMachineSettings(**profile) for profile in data]

        self.profiles = loaded_profiles
        return self

    def get_machines_settings(self, machine_model: MachineModel) -> VendingMachineProfile:

        for profile in self.profiles:
            if machine_model == profile.model:

                containers_dict: dict[ComponentName, Container] = {}

                for container in profile.containers_data:
                    component_name = ComponentName(container.component_name)

                    min_speed_dto = MixSpeed(
                        speed=DischargeSpeedStepNumber(container.min_speed.speed),
                        quantity=container.min_speed.quantity,
                    )

                    max_speed_dto = MixSpeed(
                        speed=DischargeSpeedStepNumber(container.max_speed.speed),
                        quantity=container.max_speed.quantity,
                    )

                    container_dto = Container(
                        id=container.id,
                        component_name=component_name,
                        min_speed=min_speed_dto,
                        max_speed=max_speed_dto,
                    )

                    containers_dict[component_name] = container_dto

                dto = VendingMachineProfile(
                    model=profile.model,
                    containers_data=containers_dict,
                    recipe_table_name=profile.recipe_table_name,
                    water_per_second=profile.water_per_second,
                    calibration_time=profile.calibration_time,
                    coffee_per_second=profile.coffee_per_second,
                )
                return dto

        raise Exception("Передана неизвестная модель кофемашины.")
