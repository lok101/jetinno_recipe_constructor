import enum


class TempType(enum.IntEnum):
    HOT = 1
    COLD = 0


class CupType(enum.IntEnum):
    BIG = 0
    MEDIUM = 1
    SMALL = 2


class IntensityVariable(enum.IntEnum):
    ENABLE = 1
    DISABLE = 0


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


class DischargeSpeed(enum.IntEnum):

    # todo проверить значения

    speed_1 = 20
    speed_2 = 30
    speed_3 = 40
    speed_4 = 60
    speed_5 = 70
    speed_6 = 80
    speed_7 = 90
    speed_8 = 110
    speed_9 = 120


# class ComponentType(enum.StrEnum):
#     COFFEE = ...
#     WATER = ...
#     POWDER = ...
#     COLD_POWDER = ...
#     SYRUP = ...
#     CONCENTRATE = ...
