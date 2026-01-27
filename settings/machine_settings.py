import json
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from enums import DischargeSpeed


class GramPerSecond(BaseModel):
    value: float


class DischargeSpeedItem(BaseModel):
    speed: DischargeSpeed
    quantity: GramPerSecond


class Canister:
    name: str
    calibration_value: DischargeSpeedItem


class VendingMachineProfile(BaseModel):
    model: str

    discharge_speed_settings: dict[DischargeSpeed, DischargeSpeedItem]
    canister_config: list[Canister]


class KitVendingAccountsSettings(BaseSettings):
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

    profiles: list[VendingMachineProfile] = Field(default_factory=list)

    @field_validator("accounts_file", mode="before")
    @classmethod
    def validate_accounts_file(cls, v: str | Path) -> Path:
        """Преобразует строку в Path объект."""
        if isinstance(v, str):
            return Path(v)
        return v

    @model_validator(mode="after")
    def load_profiles_from_file(self) -> "KitVendingAccountsSettings":
        loaded_profiles: list[VendingMachineProfile] = []
        if self.profiles_file.exists():
            with open(self.profiles_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    loaded_profiles = [VendingMachineProfile(**profile) for profile in data]

        self.profiles = loaded_profiles
        return self

    # def to_account_dtos(self) -> list[KitVendingAccountDTO]:
    #     """Преобразует настройки аккаунтов в список AccountDTO."""
    #     return [
    #         KitVendingAccountDTO(
    #             login=account.login,
    #             password=account.password,
    #             company_id=account.company_id,
    #             name=account.name
    #         )
    #         for account in self.accounts
    #     ]
