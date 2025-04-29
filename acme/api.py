from flask import Flask
from flask import request
# запуск сервера .\.venv\Scripts\flask --app .\acme\server.py run
app = Flask(__name__) # создает экземпляр приложения Flask


import model
import logic

_note_logic = logic.NoteLogic() # Создаём объект _note_logic, через который будем управлять заметками.


# Notes exception class
class ApiException(Exception):# кастомное исключение 
       pass
# Notes exception f-n
def _from_raw(raw_note) -> model.Note:
       parts = raw_note.split('|')
       if len(parts) == 2:
              note = model.Note()
              note.id = None
              note.title = str(parts[0])
              note.text = str(parts[1])
              return note
       elif len(parts) == 3:
              note = model.Note()
              note.id = str(parts[0])
              note.title = str(parts[1])
              note.text = str(parts[2])
              return note
       else:
              raise  ApiException(f"Invalid RAW note data {raw_note}")

def _to_raw(note: model.Note) -> str:
       if note.id is None: #такая запись более правильная с точки зрения питона
              return f"{note.title}|{note.text}"
       else:
              return f"{note.id}|{note.title}|{note.text}"

API_ROOT = "/api/v1" # добавим корень нашего API то что будет исп при вызовах
NOTE_API_ROOT = API_ROOT + "/note"

# добавим роутинг по урл
@app.route(NOTE_API_ROOT + "/", methods=["POST"])
def create():
    try:
        data = request.get_data().decode('utf-8')
        note = _from_raw(data)
        _id = _note_logic.create(note)
        return f"new id: {_id}", 201
    except Exception as ex:
        return f"failed to CREATE with: {ex}", 404

@app.route(NOTE_API_ROOT + "/", methods=["GET"])
def list():
    try:
        notes = _note_logic.list()
        raw_notes = ""
        for note in notes:
            raw_notes += _to_raw(note) + '\n'
        return raw_notes, 200
    except Exception as ex:
        return f"failed to LIST with: {ex}", 404

@app.route(NOTE_API_ROOT + "/<_id>/", methods=["GET"])
def read(_id: str):
    try:
        note = _note_logic.read(_id)
        raw_note = _to_raw(note)
        return raw_note, 200
    except Exception as ex:
        return f"failed to READ with: {ex}", 404

@app.route(NOTE_API_ROOT + "/<_id>/", methods=["PUT"])
def update(_id: str):
    try:
        data = request.get_data().decode('utf-8')
        note = _from_raw(data)
        _note_logic.update(_id, note)
        return "updated", 200
    except Exception as ex:
        return f"failed to UPDATE with: {ex}", 404

@app.route(NOTE_API_ROOT + "/<_id>/", methods=["DELETE"])
def delete(_id: str):
    try:
        _note_logic.delete(_id)
        return "deleted", 200
    except Exception as ex:
        return f"failed to DELETE with: {ex}", 404



