from src.enums import MixSpeed

DEFAULT_MIX_SPEED = MixSpeed.speed_7

WATER_ML_REP_SECOND = 10

COFFEE_SETTINGS = {
    "prebrewingTime": 2,
    "prebrewingWaterRatio": 10,
    "restorationTime": 0.2,
    "secondSqueezeForce": 90,
    "secondSqueezeTime": 2,
    "squeezeForce": 90,
    "squeezeTime": 2
}

discharge_speeds = {
    "Ваниль": ((1, 0.71), (9, 4.7)),
    "Шоколад": ((1, 0.69), (9, 4.7)),
    "Сливки": ((1, 0.59), (9, 3.8)),
}

canister_ids = {
    "N JL24": {
        "Ваниль": 1,
        "Шоколад": 3,
        "Сливки": 2,
    }
}
