import enum

COFFEE_CONTAINER_ID = 170
WATER_CONTAINER_ID = 0

class TempType(enum.IntEnum):
    HOT = 1
    COLD = 0


class CupType(enum.IntEnum):
    BIG = 0
    MEDIUM = 1
    SMALL = 2


class IntensityVariable(enum.IntEnum):
    AS_CONTAINER_OPTION = 0
    ENABLE = 1
    DISABLE = 2


class MixSpeed(enum.IntEnum):
    speed_0 = 0
    speed_1 = 20
    speed_2 = 30
    speed_3 = 40
    speed_4 = 60
    speed_5 = 70
    speed_6 = 80
    speed_7 = 90
    speed_8 = 110
    speed_9 = 120


DEFAULT_MIX_SPEED = MixSpeed.speed_5


class DischargeSpeedStepNumber(enum.IntEnum):
    step_1 = 1
    step_2 = 2
    step_3 = 3
    step_4 = 4
    step_5 = 5
    step_6 = 6
    step_7 = 7
    step_8 = 8
    step_9 = 9


class DischargeSpeed(enum.IntEnum):
    speed_1 = 20
    speed_2 = 30
    speed_3 = 40
    speed_4 = 60
    speed_5 = 70
    speed_6 = 80
    speed_7 = 90
    speed_8 = 110
    speed_9 = 120


class ComponentName(enum.StrEnum):
    WATER = "Вода"
    COFFEE = "Кофе"
    MILK = "Сливки"
    VANILLA = "Ваниль"
    CHOCO = "Шоколад"
    SUGAR = "Сахар"

    RAF_BANAN = "Раф | Банан"
    RAF_CARAMEL = "Раф | Карамель"

    VANILLA_MILKSHAKE = "МШ | Ваниль"


class MachineModel(enum.StrEnum):
    JL24 = "JL24"
    JL28 = "JL28"
    JL220 = "JL220"

POWDER_MATERIAL_ID = 10008

material_ids: dict[ComponentName, int] = {
    ComponentName.WATER: 10007,
    ComponentName.COFFEE: 10009,
    ComponentName.SUGAR: 10016,
}
