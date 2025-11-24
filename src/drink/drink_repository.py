from abc import ABC, abstractmethod

from src.drink.drink import Drink


class DrinkRepository(ABC):
    @abstractmethod
    def add(self, drink: Drink): pass

    @abstractmethod
    def get(self, drink_id: int) -> Drink | None: pass


class DrinkRepositoryImpl(DrinkRepository):
    def __init__(self):
        self._storage = {}

    def add(self, drink: Drink):
        self._storage[drink.id] = drink

    def get(self, drink_id: int) -> Drink | None:
        return self._storage.get(drink_id)
