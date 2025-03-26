Получить токен - `curl -X POST "http://0.0.0.0:8000/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=secret"`

Вывести всех пользователей - `curl -X GET "http://0.0.0.0:8000/users/list" -H "accept: application/json" -H "Authorization: Bearer <token>"`

Создать пользователя - `curl -X POST "http://0.0.0.0:8000/users/create" -H "accept: application/json" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"username":"admin1","email":"admin@example.ru","password":"secret","name":"Admin","surname":"Admin","age":30}'`

Удалить пользователя - `curl -X DELETE "http://0.0.0.0:8000/users/delete?user_id=2" -H "accept: application/json" -H "Authorization: Bearer <token>"`

Вывести все сообщения - `curl -X GET "http://0.0.0.0:8000/messages/list" -H "accept: application/json" -H "Authorization: Bearer <token>"`
