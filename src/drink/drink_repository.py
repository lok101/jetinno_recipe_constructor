from abc import ABC, abstractmethod

from src.drink.drink import Drink


class DrinkRepository(ABC):
    @abstractmethod
    def add(self, drink: Drink): pass

    @abstractmethod
    def get(self, drink_name: str) -> Drink | None: pass


class DrinkRepositoryImpl(DrinkRepository):
    def __init__(self):
        self._storage: dict[str, Drink] = {}

    def add(self, drink: Drink):
        self._storage[drink.full_name] = drink

    def get(self, drink_name: str) -> Drink | None:
        return self._storage.get(drink_name)
