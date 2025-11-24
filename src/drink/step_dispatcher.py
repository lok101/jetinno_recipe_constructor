from src.drink.step import BaseStep


class StepsDispatcher:
    def __init__(self):
        self._map = {}

    def register_component(self, component_name: str, step_type: type[BaseStep]):
        if component_name in self._map.keys():
            raise Exception(f"Компонент: \"{component_name}\" - уже зарегистрирован.")

        self._map[component_name] = step_type

    def get_step_type(self, component_name: str) -> BaseStep:
        if component_name not in self._map.keys():
            raise Exception(f"Для компонента: \"{component_name}\" - не зарегистрирован тип шага.")

        return self._map.get(component_name)


