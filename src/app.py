from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from domain.exceptions import ContainerConflictError
from src.domain.entities.machine_drink import MachineDrink
from src.domain.entities.vending_machine_profile import VendingMachineProfile
from src.domain.enums import MachineModel, ComponentName
from settings.vending_machines_settings import MachineProfilesSettings

profiles = MachineProfilesSettings()


class DrinksDataPort(Protocol):
    def get_machine_drinks(self, machine_profile: VendingMachineProfile) -> list[MachineDrink]: pass


class SaveDrinksAsFile(Protocol):
    def save_to_file(self, drinks: list[MachineDrink], file_name: str): pass


class SaveContainersAsFile(Protocol):
    def save_to_json(self, machine_profile: VendingMachineProfile, used_component_names: set[ComponentName]): pass


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

        # Фильтруем напитки по enabled=True
        enabled_drinks = [drink for drink in machine_drinks if drink.enabled]

        # Проверяем конфликты контейнеров и собираем используемые canister_id
        used_canister_ids = self._validate_and_collect_containers(enabled_drinks)

        # Сохраняем только используемые контейнеры
        self.save_canister_config.save_to_json(machine_profile=machine_data, used_component_names=used_canister_ids)

        # Сохраняем только напитки с enabled=True
        self.recipes_constructor.save_to_file(enabled_drinks, file_name)
        self.products_constructor.save_to_file(enabled_drinks, file_name)

    @staticmethod
    def _validate_and_collect_containers(drinks: list[MachineDrink]) -> set[ComponentName]:
        container_mapping: dict[int, set[ComponentName]] = {}
        used_component_names: set[ComponentName] = set()

        for drink in drinks:
            for step in drink.steps:
                canister_id: int = step.canister_id
                component_name: ComponentName = ComponentName(step.name)

                used_component_names.add(component_name)

                if canister_id not in container_mapping:
                    container_mapping[canister_id] = set()

                container_mapping[canister_id].add(component_name)

        conflicts = []
        for canister_id, component_names in container_mapping.items():
            if len(component_names) > 1:
                conflicts.append(
                    f"Контейнер с id={canister_id} используется с разными именами: {', '.join(sorted(component_names))}"
                )

        if conflicts:
            raise ContainerConflictError(
                "Обнаружены конфликты контейнеров:\n" + "\n".join(conflicts)
            )

        return used_component_names
