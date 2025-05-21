Для Windows
  Запуск flask:
    .\.venv\Scripts\flask.exe --app .\pythonProject\acme\server.py run

  Проверка через утилиту Postman
### добавление новой заметки
    метод          POST 
    поле ввода     localhost:5000/api/v1/calendar/
    body           "3|2025-05-06|titl|text"
  Вывод присвоение id (new id: 3) или ошибка формата даты, одно событие на дату
### получение всего списка заметок
    метод    GET
    адрес    localhost:5000/api/v1/calendar/
    Выводит список событий в формате
      1|2025-05-06|titl|text"
      2|2025-5-06|titl|text"
      3|2025-05-07|titl|text"
### получение заметки по идентификатору / ID == 1
    метод    GET
    адрес    localhost:5000/api/v1/calendar/1
### обновление текста заметки по идентификатору / ID == 3 /   
    метод   PUT
    адрес   localhost:5000/api/v1/calendar/3
    поле Body : "3|2025-07-08|ti1l|te1t"
### удаление заметки по идентификатору / ID == 1
  метод   DELETE
  адрес формата    localhost:5000/api/v1/calendar/1





