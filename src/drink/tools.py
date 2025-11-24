import math

from src.config import DEFAULT_MIX_SPEED, canister_ids, discharge_speeds, WATER_ML_REP_SECOND
from src.enums import CupType, TempType, IntensityVariable, MixSpeed, DischargeSpeed


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


# def get_mix_speed(component_name: str) -> MixSpeed | None:
#     if component_name == "Кофе":
#         return
#     if component_name == "Вода":
#         return
#
#     return mix_speeds.get(component_name, DEFAULT_MIX_SPEED)
#
#
# def get_temp_type(component_name: str) -> TempType | None:
#     if component_name == "Кофе":
#         return
#     if component_name == "Вода":
#         return
#
#     return temp_types.get(component_name, DEFAULT_TEMP_TYPE)
#
#
# def get_intensity_variables(component_name: str) -> IntensityVariable:
#     return intensity_variables.get(component_name, DEFAULT_INTENSITY_VARIABLE)


def get_discharge_speed(component_name: str, component_weight: int, water_volume: int) -> DischargeSpeed | None:
    if component_name in ("Кофе", "Вода"):
        return None

    speeds_list = list(DischargeSpeed)
    cds = discharge_speeds.get(component_name)

    if cds is None:
        raise Exception(f"Не найдены параметры скорость подачи для ингредиента \"{component_name}\"")

    (min_step, min_gr), (max_step, max_gr) = cds

    step_time = water_volume / WATER_ML_REP_SECOND - 1
    gr_per_second = component_weight / step_time

    if gr_per_second < min_gr:
        return DischargeSpeed.speed_1

    speed_step = (max_gr - min_gr) / (max_step - min_step)
    speed_regulator_number = math.ceil((gr_per_second - min_gr) / speed_step)
    return speeds_list[speed_regulator_number]
