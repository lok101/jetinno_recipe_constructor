from src.drink.drink_repository import DrinkRepository
from src.drink.step_dispatcher import StepsDispatcher
from src.models import DrinkModel
from src.drink.drink import Drink
from src.drink.tools import get_cup_type, get_canister_id, get_discharge_speed


class DrinkService:
    def __init__(self, drinks_repository: DrinkRepository, step_dispatcher: StepsDispatcher):
        self._step_dispatcher = step_dispatcher
        self._drinks_repository = drinks_repository

    def get_drink_or_ex(self, drink_id: int) -> Drink:
        drink = self._drinks_repository.get(drink_id)

        if drink is None:
            raise Exception(f"Не найден напиток с переданным номером: {drink_id}.")

        return drink

    def create_drinks(self, drinks_data: list[DrinkModel], machine_model: str):
        for drink_model in drinks_data:
            drink_data = drink_model.model_dump()

            steps = []

            for i, step_model in enumerate(drink_model.steps):
                step_data = step_model.model_dump()

                component_name = step_model.name

                step_data["order"] = i
                step_data["canister_id"] = get_canister_id(machine_model=machine_model, component_name=component_name)
                step_data["discharge_speed"] = get_discharge_speed(
                    component_name=component_name,
                    component_weight=step_model.component_weight,
                    water_volume=step_model.water_volume
                )

                step_type = self._step_dispatcher.get_step_type(component_name)
                step = step_type.model_validate(step_data)
                steps.append(step)

            drink_data["steps"] = steps
            drink_data["cup_type"] = drink_model.cup_type

            if drink_model.cup_type is None:
                drink_data["cup_type"] = get_cup_type(capacity=drink_model.capacity)

            drink = Drink.model_validate(drink_data)

            self._drinks_repository.add(drink)
