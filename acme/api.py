
from flask import Flask
from flask import request
# запуск сервера .\.venv\Scripts\flask --app .\acme\server.py run
app = Flask(__name__) # создает экземпляр приложения Flask


import model
import logic

_event_logic = logic.EventLogic() # Создаём объект _note_logic, через который будем управлять заметками.


# Notes exception class
class ApiException(Exception):# кастомное исключение в нем нет логики, необходим для исключения при конвертации строки
       pass
# Notes exception f-n
def _from_raw(raw_event) -> model.Event: #берет текстовую строку и возвращает
       parts = raw_event.split('|') # строка в список
       if len(parts) == 3:
              event = model.Event()
              event.id = None
              event.date = str(parts[0])
              event.title = str(parts[1])
              event.text = str(parts[2])
              return event
       elif len(parts) == 4:
              event = model.Event()
              event.id = str(parts[0])
              event.date = str(parts[1])
              event.title = str(parts[2])
              event.text = str(parts[3])
              return event
       else:
              raise  ApiException(f"Invalid RAW note data {raw_event}")

def _to_raw(event: model.Event) -> str: # обратное для возврата
       if event.id is None: #такая запись более правильная с точки зрения питона
              return f"{event.date}|{event.title}|{event.text}" # если нет Id возвращает только 2 значения в виде строки
       else:
              return f"{event.id}|{event.date}|{event.title}|{event.text}"

API_ROOT = "/api/v1" # Добавим корень нашего API то что будет исп. При вызовах
EVENT_API_ROOT = API_ROOT + "/event"

# добавим роутинг по урл
@app.route(EVENT_API_ROOT + "/", methods=["POST"]) # это декоратор во Flask, который связывает URL-адрес (маршрут) с функцией, которую должен вызывать сервер при обращении к этому адресу.
def create():
    try:
        data = request.get_data().decode('utf-8')
        event = _from_raw(data)
        _id = _event_logic.create(event)
        return f"new id: {_id}", 201 # 201 для http используется при создании заметок
    except Exception as ex:
        return f"failed to CREATE with: {ex}", 404

@app.route(EVENT_API_ROOT + "/", methods=["GET"])
def list(): # list имя встроенной переменной
    try:
        events = _event_logic.list()
        raw_events = ""
        for event in events:
            raw_events += _to_raw(event) + '\n'
        return raw_events, 200
    except Exception as ex:
        return f"failed to LIST with: {ex}", 404

@app.route(EVENT_API_ROOT + "/<_id>/", methods=["GET"]) # нижнее подч, чтобы не было с сист ф-ми путаницы
def read(_id: str):
    try:
        event = _event_logic.read(_id)
        raw_event = _to_raw(event)
        return raw_event, 200
    except Exception as ex:
        return f"failed to READ with: {ex}", 404

@app.route(EVENT_API_ROOT + "/<_id>/", methods=["PUT"])
def update(_id: str):
    try:
        data = request.get_data().decode('utf-8')
        event = _from_raw(data)
        _event_logic.update(_id, event)
        return "updated", 200
    except Exception as ex:
        return f"failed to UPDATE with: {ex}", 404

@app.route(EVENT_API_ROOT + "/<_id>/", methods=["DELETE"])
def delete(_id: str):
    try:
        _event_logic.delete(_id)
        return "deleted", 200
    except Exception as ex:
        return f"failed to DELETE with: {ex}", 404



