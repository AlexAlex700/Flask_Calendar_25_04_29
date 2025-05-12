from typing import List
from datetime import datetime

import model
import db

TITLE_LIMIT = 30# для теста ставим
TEXT_LIMIT = 200# для теста ставим

class LogicException(Exception):
    pass

class EventLogic:
    def __init__(self):
        self._event_db = db.EventDB()

    @staticmethod # проверка ограничения по длине
    def _validate_event(event: model.Event, existing_events: List[model.Event] = None): #функция ограничений из тз
        if event is None:
            raise LogicException("event is None")
        if event.title is None or len(event.title) > TITLE_LIMIT:
            raise LogicException(f"title length > MAX: {TITLE_LIMIT}")
        if event.text is None or len(event.text) > TEXT_LIMIT:
            raise LogicException(f"text length > MAX: {TEXT_LIMIT}")


            # Проверка корректности формата даты
        try:
            datetime.strptime(event.date, "%Y-%m-%d")
        except ValueError:
            raise LogicException("Invalid date format. Expected YYYY-MM-DD.")
        # Проверка уникальности даты, если передан список существующих событий
        if existing_events:
            for ev in existing_events:
                if ev.date == event.date and ev.id != event.id:
                    raise LogicException("Only one event per day is allowed.")

    def create(self, event: model.Event) -> str:
        all_events = self._event_db.list()
        self._validate_event(event, all_events)
        try:
            return self._event_db.create(event)
        except Exception as ex:
            raise LogicException(f"failed CREATE logic with: {ex}")

    def list(self) -> List[model.Event]:
        try:
            return self._event_db.list()
        except Exception as ex:
            raise LogicException(f"failed LIST operation with: {ex}")

    def read(self, _id: str) -> model.Event:
        try:
            return self._event_db.read(_id)
        except Exception as ex:
            raise LogicException(f"failed READ operation with: {ex}")

    def update(self, _id: str, event: model.Event):
        all_events = self._event_db.list()
        event.id = _id  # временно подставим ID, чтобы исключить его при проверке уникальности
        self._validate_event(event, all_events)
        try:
            return self._event_db.update(_id, event)
        except Exception as ex:
            raise LogicException(f"failed UPDATE operation with: {ex}")


    def delete(self, _id: str):
        try:
            return self._event_db.delete(_id)
        except Exception as ex:
            raise LogicException(f"failed DELETE operation with: {ex}")
