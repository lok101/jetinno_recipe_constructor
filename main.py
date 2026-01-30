import os

from pydantic import BaseModel

from adapters.get_machine_products import get_machine_drinks
from enums import MachineModel
from settings.vending_machines_settings import MachineProfilesSettings

from src.drink.step import CoffeeStep, WaterStep, PowderStep, ColdPowderStep, SugarStep
from src.drink.step_dispatcher import StepsDispatcher
from src.drink.drink_repository import DrinkRepository, DrinkRepositoryImpl

drink_repo: DrinkRepository = DrinkRepositoryImpl()
step_dispatcher = StepsDispatcher()

step_dispatcher.register_component("Кофе", CoffeeStep)
step_dispatcher.register_component("Вода", WaterStep)
step_dispatcher.register_component("Сливки", PowderStep)
step_dispatcher.register_component("Шоколад", PowderStep)
step_dispatcher.register_component("Ваниль", PowderStep)
step_dispatcher.register_component("Сахар", SugarStep)
step_dispatcher.register_component("МШ | Ваниль", ColdPowderStep)


def _save_to_file(data: list[BaseModel], file_name: str, file_type: str):
    os.makedirs("Jetinno", exist_ok=True)
    with open(f'Jetinno/{file_name}.{file_type}', 'wb') as file:
        data = f'[{", ".join([item.model_dump_json(by_alias=True, exclude_none=True) for item in data])}]'
        bytes_data = str(data).encode('utf-8')
        file.write(bytes_data)


def main():
    machine_model = MachineModel.JL28
    profiles = MachineProfilesSettings()

    machine_data = profiles.get_machines_settings(machine_model)

    # drinks_data: list[DrinkModel] = get_drinks_data()

    drinks_data = get_machine_drinks(machine_data.recipe_table_name)
    pass

    # drink_service.create_drinks(drinks_data=drinks_data, machine_settings=machine_data)

    # products_data: list[ProductModel] = get_products_data(machine_model)
    products = products_service.create_products(products_data)
    recipes = recipe_service.create_recipes(products_data)

    for item in products: print(item.pic_path)

    _save_to_file(products, machine_model, "product")
    _save_to_file(recipes, machine_model, "recipe")
    pass


if __name__ == "__main__":
    main()
