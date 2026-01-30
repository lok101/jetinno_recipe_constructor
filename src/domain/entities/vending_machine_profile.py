from dataclasses import dataclass

from src.domain.entities.container import Container
from src.domain.enums import ComponentName, DischargeSpeed
from src.dtos.container_data_dto import CoffeeContainerDataDTO, WaterContainerDataDTO, BaseContainerDataDTO


@dataclass(frozen=True, slots=True)
class VendingMachineProfile:
    model: str
    recipe_table_name: str
    water_per_second: int
    calibration_time: int
    coffee_per_second: float
    containers_data: dict[ComponentName, Container]

    def _get_container(self, component_name: ComponentName) -> Container:
        container = self.containers_data.get(component_name)

        if container is not None:
            return container

        raise KeyError(
            {
                "message": "Не найдена конфигурация для контейнера с переданным именем.",
                "component": component_name,
                "machine_model": self.model,
            }
        )

    def get_container_id(self, component_name: ComponentName) -> int:
        if component_name is ComponentName.COFFEE:
            return 170

        if component_name is ComponentName.WATER:
            return 0

        return self._get_container(component_name).id

    def get_discharge_speed(
            self,
            component_name: ComponentName,
            component_weight: int,
            water_volume: int
    ) -> DischargeSpeed | None:

        if component_name in (ComponentName.COFFEE, ComponentName.WATER):
            return None

        container = self._get_container(component_name)
        return container.get_discharge_speed(component_weight, water_volume, self.water_per_second)

    def get_containers_parameters(self) -> list[BaseContainerDataDTO]:

        res: list[BaseContainerDataDTO] = []

        coffee_container: CoffeeContainerDataDTO = Container.get_coffee_container(
            calibration_time=self.calibration_time,
            calibration_value=self.coffee_per_second
        )

        water_container: WaterContainerDataDTO = Container.get_water_container()

        res.append(coffee_container)
        res.append(water_container)

        for container in self.containers_data.values():
            res.append(
                container.as_container_data_dto(calibration_time=self.calibration_time)
            )

        return res
