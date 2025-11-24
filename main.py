import os

from pydantic import BaseModel

from src.drink.drink_service import DrinkService
from src.drink.step import CoffeeStep, WaterStep, PowderStep
from src.drink.step_dispatcher import StepsDispatcher
from src.models import DrinkModel, ProductModel
from src.drink.drink_repository import DrinkRepository, DrinkRepositoryImpl
from src.get_sheet_data import get_drinks_data, get_products_data
from src.product.product_service import ProductService
from src.recipe.recipe_service import RecipeService

drink_repo: DrinkRepository = DrinkRepositoryImpl()
step_dispatcher = StepsDispatcher()
drink_service = DrinkService(drink_repo, step_dispatcher)

products_service = ProductService(drink_service)
recipe_service = RecipeService(drink_service)

step_dispatcher.register_component("Кофе", CoffeeStep)
step_dispatcher.register_component("Вода", WaterStep)
step_dispatcher.register_component("Сливки", PowderStep)
step_dispatcher.register_component("Шоколад", PowderStep)
step_dispatcher.register_component("Ваниль", PowderStep)


def _save_to_file(data: list[BaseModel], file_name: str, file_type: str):
    os.makedirs("Jetinno", exist_ok=True)
    with open(f'Jetinno/{file_name}.{file_type}', 'wb') as file:
        data = f'[{", ".join([item.model_dump_json(by_alias=True, exclude_none=True) for item in data])}]'
        bytes_data = str(data).encode('utf-8')
        file.write(bytes_data)


def main():
    machine_model = "N JL24"

    drinks_data: list[DrinkModel] = get_drinks_data()
    drink_service.create_drinks(drinks_data=drinks_data, machine_model=machine_model)

    products_data: list[ProductModel] = get_products_data(machine_model)
    products = products_service.create_products(products_data)
    recipes = recipe_service.create_recipes(products_data)

    _save_to_file(products, machine_model, "product")
    _save_to_file(recipes, machine_model, "recipe")
    pass


if __name__ == "__main__":
    main()
