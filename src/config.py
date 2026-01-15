from src.enums import MixSpeed

DEFAULT_MIX_SPEED = MixSpeed.speed_5

WATER_ML_REP_SECOND = 10

COFFEE_SETTINGS = {
    "prebrewingTime": 0,
    "prebrewingWaterRatio": 0,
    "restorationTime": 0.3,
    "secondSqueezeForce": 90,
    "secondSqueezeTime": 2,
    "squeezeForce": 90,
    "squeezeTime": 2
}

discharge_speeds = {
    "Ваниль": ((3, 1.77), (9, 4.65)),
    "Шоколад": ((3, 1.75), (9, 4.76)),
    "Сливки": ((3, 1.42), (9, 3.8)),
}

canister_ids = {
    "N JL24": {
        "Ваниль": 1,
        "Шоколад": 3,
        "Сливки": 2,
    }
}
