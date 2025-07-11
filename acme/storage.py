# Управление будет по _id ?
# 25_05_01 Заменены note и модель Note
from typing import List #List используется для аннотации типов (в частности — возвращаемого списка заметок).

import model

class StorageException(Exception):
    pass

class LocalStorage: # хранение данных в памяти в виде словаря
    def __init__(self):
        self._id_counter = 0
        self._storage = {}

    def create(self, calendar: model.Event) -> str: # увеличивает счетчик и присваевает id
        self._id_counter += 1
        calendar.id = str(self._id_counter)
        self._storage[calendar.id] = calendar
        return calendar.id

    def list(self) -> List[model.Event]:# Возвращает все заметки, как список.
        return list(self._storage.values())

    def read(self, _id: str) -> model.Event:
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        return self._storage[_id]

    def update(self, _id: str, calendar: model.Event):
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        calendar.id = _id
        self._storage[calendar.id] = calendar

    def delete(self, _id: str):
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        del self._storage[_id]