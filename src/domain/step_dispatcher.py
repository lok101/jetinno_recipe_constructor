from src.domain.entities.step import BaseStep
from src.domain.enums import ComponentName


class StepsDispatcher:
    def __init__(self):
        self._map = {}

    def register_component(self, component_name: ComponentName, step_type: type[BaseStep]) -> None:
        if component_name in self._map.keys():
            raise Exception(f"Компонент: \"{component_name}\" - уже зарегистрирован.")

        self._map[component_name] = step_type

    def get_step_type(self, component_name: ComponentName) -> BaseStep:
        if component_name not in self._map.keys():
            raise Exception(f"Для компонента: \"{component_name}\" - не зарегистрирован тип шага.")

        return self._map.get(component_name)
