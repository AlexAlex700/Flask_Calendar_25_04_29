# Интерфейс к хранилищу, проксирует все обращения к storage, здесь нет никакой логики
from typing import List

import model
import storage

class DBException(Exception):# exeption уровня db уровень логики должен от слоя bd ждать, а не от сторадж
    pass

class EventDB:
    def __init__(self):
        self._storage = storage.LocalStorage()

    def create(self, calendar: model.Event) -> str:
        try:
            return self._storage.create(calendar)
        except Exception as ex:
            raise DBException(f"failed CREATE operation with: {ex}")

    def list(self) -> List[model.Event]:
        try:
            return self._storage.list()
        except Exception as ex:
            raise DBException(f"failed LIST operation with: {ex}")

    def read(self, _id: str) -> model.Event:
        try:
            return self._storage.read(_id)
        except Exception as ex:
            raise DBException(f"failed READ operation with: {ex}")

    def update(self, _id: str, calendar: model.Event):
        try:
            self._storage.update(_id, calendar)
        except Exception as ex:
            raise DBException(f"failed UPDATE operation with: {ex}")

    def delete(self, _id: str):
        try:
            return self._storage.delete(_id)
        except Exception as ex:
            raise DBException(f"failed DELETE operation with: {ex}")