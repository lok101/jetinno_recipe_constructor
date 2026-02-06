import os
from abc import ABC, abstractmethod
from typing import Annotated

from pydantic import BaseModel, Field

from src.domain.entities.machine_drink import MachineDrink
from src.domain.entities.step import BaseStep, PowderStep
from src.domain.enums import DrinkTempType

COFFEE_SETTINGS = {
    "prebrewingTime": 0,
    "prebrewingWaterRatio": 0,
    "restorationTime": 0.3,
    "secondSqueezeForce": 90,
    "secondSqueezeTime": 2,
    "squeezeForce": 90,
    "squeezeTime": 2
}


class RecipeStep(BaseModel):
    name: Annotated[str, Field(serialization_alias="component_name")]
    order: Annotated[int, Field(serialization_alias="recipeOutOrder")]
    water_volume: Annotated[int, Field(serialization_alias="waterVolume")]
    canister_id: Annotated[int, Field(serialization_alias="canisterId")]

    component_weight: Annotated[int | None, Field(serialization_alias="gradientWeight", default=None)]
    mix_speed: Annotated[int | None, Field(serialization_alias="mixSpeed", default=None)]
    temp_type: Annotated[int | None, Field(serialization_alias="tempType", default=None)]
    discharge_speed: Annotated[int | None, Field(serialization_alias="dischargeSpeed", default=None)]

    is_showed: Annotated[int, Field(serialization_alias="isShowed", default=1)]
    add_recipe_tyme: Annotated[int, Field(serialization_alias="addRecipeTime", default=0)]
    delay_time: Annotated[int, Field(serialization_alias="delayTime", default=60)]


class Recipe(BaseModel):
    recipe_name: Annotated[str, Field(serialization_alias="recipeName")]
    canister_ids_str: Annotated[str, Field(serialization_alias="canisterIds")]
    is_checked: Annotated[bool, Field(serialization_alias="isChecked")]
    steps: Annotated[list[RecipeStep], Field(serialization_alias="stepses")]
    es_attr: Annotated[dict | None, Field(serialization_alias="esAttr")]


class Product(BaseModel):
    id: Annotated[int, Field(serialization_alias="productId")]
    name: Annotated[str, Field(serialization_alias="nameCN")]
    capacity: Annotated[int, Field(serialization_alias="cupCapacity")]
    cup_type: Annotated[int, Field(serialization_alias="cupType")]
    order: Annotated[int, Field(serialization_alias="order")]
    price: Annotated[int, Field(serialization_alias="price")]
    recipe_name: Annotated[str, Field(serialization_alias="recipeName")]
    pic_path: Annotated[str, Field(serialization_alias="picPath")]
    canister_ids_str: Annotated[str, Field(serialization_alias="canisterIds")]
    drink_temp_type: Annotated[str, Field(serialization_alias="hotCold")]

    make_time: Annotated[int, Field(serialization_alias="makeTime")]
    enable: Annotated[bool, Field(serialization_alias="enable")]
    best_sell: Annotated[bool, Field(serialization_alias="bestSell")]
    save_out: Annotated[bool, Field(serialization_alias="saveOut")]
    visible: Annotated[bool, Field(serialization_alias="visible")]


class SaveDrinksAsFile(ABC):
    @abstractmethod
    def save_to_file(self, drinks: list[MachineDrink], file_name: str) -> None: pass

    @staticmethod
    def _save_to_file(data: list[BaseModel], file_name: str, file_type: str):
        os.makedirs("Jetinno", exist_ok=True)
        with open(f'Jetinno/{file_name}.{file_type}', 'wb') as file:
            json_data = f'[{", ".join([item.model_dump_json(by_alias=True, exclude_none=True) for item in data])}]'
            bytes_data = json_data.encode('utf-8')
            file.write(bytes_data)


class SaveDrinksAsRecipesPackAdapter(SaveDrinksAsFile):
    def save_to_file(self, drinks: list[MachineDrink], file_name: str) -> None:
        recipes = [self._create_recipe(drink) for drink in drinks]
        self._save_to_file(recipes, file_name, "recipe")

    def _create_recipe(self, drink: MachineDrink) -> Recipe:
        recipe_steps = [self._create_recipe_step(step) for step in drink.steps]
        canister_ids_str = drink.get_canister_ids_str()
        es_attr = self._get_es_attr(drink.steps)

        return Recipe(
            recipe_name=drink.recipe_name,
            canister_ids_str=canister_ids_str,
            is_checked=True,
            steps=recipe_steps,
            es_attr=es_attr,
        )

    @staticmethod
    def _create_recipe_step(step: BaseStep) -> RecipeStep:
        component_weight = getattr(step, "component_weight", None)
        mix_speed = None
        temp_type = None
        discharge_speed = None

        if isinstance(step, PowderStep):
            mix_speed = step.mix_speed.value
            temp_type = step.temp_type.value
            discharge_speed = step.discharge_speed.value

        is_showed = step.is_intensity_variable.value

        return RecipeStep(
            name=step.name,
            order=step.order,
            water_volume=step.water_volume,
            canister_id=step.canister_id,
            component_weight=component_weight,
            mix_speed=mix_speed,
            temp_type=temp_type,
            discharge_speed=discharge_speed,
            is_showed=is_showed,
            add_recipe_tyme=step.add_recipe_time,
            delay_time=step.delay_time,
        )

    @staticmethod
    def _get_es_attr(steps: list[BaseStep]) -> dict | None:
        for step in steps:
            if step.canister_id == 170:
                return COFFEE_SETTINGS
        return None


class SaveDrinkAsProductPackAdapter(SaveDrinksAsFile):
    def save_to_file(self, drinks: list[MachineDrink], file_name: str):
        products = [self._create_product(drink) for drink in drinks]
        self._save_to_file(products, file_name, "product")

    @staticmethod
    def _create_product(drink: MachineDrink) -> Product:
        canister_ids: str = drink.get_canister_ids_str()
        pic_path: str = drink.pic_path
        temp_type: DrinkTempType = drink.get_drink_temp_type()
        visible: bool = drink.is_active

        return Product(
            id=drink.id,
            name=drink.name,
            capacity=drink.capacity,
            cup_type=drink.cup_type,
            order=drink.order,
            price=drink.price,
            recipe_name=drink.recipe_name,
            pic_path=pic_path,
            canister_ids_str=canister_ids,
            drink_temp_type=str(temp_type),

            make_time=60,
            enable=True,
            best_sell=False,
            save_out=True,
            visible=visible,
        )
