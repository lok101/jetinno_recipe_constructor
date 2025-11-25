from typing import Annotated

from pydantic import BaseModel, Field

from src.drink.drink_service import DrinkService
from src.drink.drink import Drink
from src.models import ProductModel


class RecipeStep(BaseModel):
    name: Annotated[str, Field(serialization_alias="component_name")]
    order: Annotated[int, Field(serialization_alias="recipeOutOrder")]
    water_volume: Annotated[int, Field(serialization_alias="waterVolume")]
    canister_id: Annotated[int, Field(serialization_alias="canisterId")]

    component_weight: Annotated[int, Field(serialization_alias="gradientWeight", default=None)]
    mix_speed: Annotated[int, Field(serialization_alias="mixSpeed", default=None)]
    temp_type: Annotated[int, Field(serialization_alias="tempType", default=None)]
    discharge_speed: Annotated[int, Field(serialization_alias="dischargeSpeed", default=None)]

    is_showed: Annotated[
        int, Field(serialization_alias="isShowed", default=True, validation_alias="is_intensity_variable")]
    add_recipe_tyme: Annotated[int, Field(serialization_alias="addRecipeTime", default=0)]
    delay_time: Annotated[int, Field(serialization_alias="delayTime", default=60)]


class Recipe(BaseModel):
    recipe_name: Annotated[str, Field(serialization_alias="recipeName")]
    canister_ids_str: Annotated[str, Field(serialization_alias="canisterIds")]
    is_checked: Annotated[bool, Field(serialization_alias="isChecked")]
    steps: Annotated[list[RecipeStep], Field(serialization_alias="stepses")]
    es_attr: Annotated[dict | None, Field(serialization_alias="esAttr")]


class RecipeService:
    def __init__(self, drink_service: DrinkService):
        self._drink_service = drink_service

    def create_recipes(self, products_data: list[ProductModel]) -> list[Recipe]:
        res = []

        for item in products_data:
            drink = self._drink_service.get_drink_or_ex(item.drink_id)
            recipe = self._create_jetinno_recipe(drink)
            res.append(recipe)

        return res

    @staticmethod
    def _create_jetinno_recipe(drink: Drink):
        return Recipe.model_validate(drink, from_attributes=True)
