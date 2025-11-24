from typing import Annotated

from pydantic import BaseModel, Field, BeforeValidator

from src.drink.drink_service import DrinkService
from src.models import ProductModel


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

    make_time: Annotated[int, Field(serialization_alias="makeTime", default=60)]
    enable: Annotated[bool, Field(serialization_alias="enable", default=True)]
    best_sell: Annotated[bool, Field(serialization_alias="bestSell", default=True)]
    save_out: Annotated[bool, Field(serialization_alias="saveOut", default=True)]
    visible: Annotated[bool, Field(serialization_alias="visible", default=True)]

    date: Annotated[str, Field(validation_alias="updated"), BeforeValidator(lambda dt: dt.strftime("%Y%m%d %H:%M"))]


class ProductService:
    def __init__(self, drink_service: DrinkService):
        self._drink_service = drink_service

    def create_products(self, products_data: list[ProductModel]) -> list[Product]:
        res = []

        for i, item in enumerate(products_data, 1):
            drink = self._drink_service.get_drink_or_ex(item.drink_id)
            drink_data = drink.model_dump()

            drink_data["order"] = i
            drink_data["matrix_id"] = item.matrix_id
            drink_data["price"] = item.price
            drink_data["visible"] = item.visible

            product = Product.model_validate(drink_data)
            res.append(product)

        return res
