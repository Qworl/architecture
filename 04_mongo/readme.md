Получить токен - `curl -X POST "http://0.0.0.0:8000/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=secret"`

Вывести всех пользователей - `curl -X GET "http://0.0.0.0:8000/users/list" -H "accept: application/json" -H "Authorization: Bearer <token>"`

Детали пользователя - `curl -X GET "http://0.0.0.0:8000/users/details?user_id=5" -H "accept: application/json" -H "Authorization: Bearer <token>"`

Поиск по логину - `curl -X GET "http://0.0.0.0:8000/users/list?login=admin" -H "accept: application/json" -H "Authorization: Bearer <token>`

Поиск по имени - `curl -X GET "http://0.0.0.0:8000/users/list?name=Test" -H "accept: application/json" -H "Authorization: Bearer <token>`

Поиск по имени и фамилии - `curl -X GET "http://0.0.0.0:8000/users/list?name=Test&surname=User1" -H "accept: application/json" -H "Authorization: Bearer <token>`

Создать пользователя - `curl -X POST "http://0.0.0.0:8000/users/create" -H "accept: application/json" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"username":"admin1","email":"admin@example.ru","password":"secret","name":"Admin","surname":"Admin","age":30}'`

Изменить пользователя - `curl -X PUT "http://0.0.0.0:8000/users/update?user_id=5" -H "accept: application/json" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"username":"admin1","email":"admin@example.ru","password":"secret","name":"Admin","surname":"AdminCorrected","age":30}'`

Удалить пользователя - `curl -X DELETE "http://0.0.0.0:8000/users/delete?user_id=5" -H "accept: application/json" -H "Authorization: Bearer <token>"`

Вывести все сообщения - `curl -X GET "http://0.0.0.0:8001/messages/list" -H "accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc0NTUwNzUzOX0.g3TtQSZUW0HdBZQZgSUYrFOygD2pYpbWo6I-DXazQL4"`
