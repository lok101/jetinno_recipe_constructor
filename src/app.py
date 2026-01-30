from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from src.domain.entities.machine_drink import MachineDrink
from src.domain.entities.vending_machine_profile import VendingMachineProfile
from src.domain.enums import MachineModel
from settings.vending_machines_settings import MachineProfilesSettings

profiles = MachineProfilesSettings()


class DrinksDataPort(Protocol):
    def get_machine_drinks(self, machine_profile: VendingMachineProfile) -> list[MachineDrink]: pass


class SaveDrinksAsFile(Protocol):
    def save_to_file(self, drinks: list[MachineDrink], file_name: str): pass


class SaveContainersAsFile(Protocol):
    def save_to_json(self, machine_profile: VendingMachineProfile): pass


def get_file_name(machine_name: str, timestamp: datetime) -> str:
    return f"{machine_name}_{timestamp.strftime('%Y.%m.%d %H.%M')}"


@dataclass(frozen=True, slots=True)
class Application:
    drinks_data_port: DrinksDataPort

    recipes_constructor: SaveDrinksAsFile
    products_constructor: SaveDrinksAsFile
    save_canister_config: SaveContainersAsFile

    def run(self, machine_model: MachineModel):
        file_name: str = get_file_name(machine_model.name, datetime.now())

        machine_data = profiles.get_machines_settings(machine_model)

        machine_drinks: list[MachineDrink] = self.drinks_data_port.get_machine_drinks(machine_data)

        self.save_canister_config.save_to_json(machine_profile=machine_data)
        self.recipes_constructor.save_to_file(machine_drinks, file_name)
        self.products_constructor.save_to_file(machine_drinks, file_name)
