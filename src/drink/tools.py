import math

from src.config import canister_ids, discharge_speeds, WATER_ML_REP_SECOND
from src.enums import CupType, DischargeSpeed


def get_cup_type(capacity: int):
    if capacity == 250:
        return CupType.SMALL
    if capacity == 300:
        return CupType.MEDIUM
    if capacity == 350:
        return CupType.BIG

    raise Exception(f"Стакан имеет не стандартный объём: {capacity}мл. Укажите тип стакана вручную.")


def get_canister_id(machine_model: str, component_name: str) -> int:
    if component_name == "Кофе":
        return 170
    if component_name == "Вода":
        return 0

    canister_id = canister_ids.get(machine_model, {}).get(component_name)
    if canister_id is None:
        raise Exception(f"Не найден Id для компонента: {component_name}. Модель машины: {machine_model}.")

    return canister_id


def get_discharge_speed(drink_name: str, component_name: str, component_weight: int,
                        water_volume: int) -> DischargeSpeed | None:
    if component_name in ("Кофе", "Вода"):
        return None

    speeds_list = list(DischargeSpeed)
    cds = discharge_speeds.get(component_name)

    if cds is None:
        raise Exception(f"Не найдены параметры скорость подачи для ингредиента \"{component_name}\"")

    (min_step, min_gr), (max_step, max_gr) = cds

    step_time = water_volume / WATER_ML_REP_SECOND - 1
    gr_per_second = component_weight / step_time

    linear_k = (max_gr - min_gr) / (max_step - min_step)
    linear_b = max_gr - max_step * linear_k

    speed = (gr_per_second - linear_b) / linear_k

    if speed % 1 < 0.2:
        print(
            f"Компонент \"{component_name}\" в напитке \"{drink_name}\", "
            f"слишком большой разрыв скорости подачи. Возможно большое количество воды в конце шага."
        )

    speed_index = math.ceil(speed) - 1

    if speed_index < 0:
        raise Exception("Индекс скорости подачи порошка не должен быть отрицательным.")

    try:
        discharge_speed = speeds_list[speed_index]

    except IndexError:
        print(
            f"Компонент \"{component_name}\" в напитке \"{drink_name}\", "
            f"требуемая скорость: {gr_per_second}. Максимальная: {max_gr}."
        )
        return speeds_list[-1]

    return discharge_speed
