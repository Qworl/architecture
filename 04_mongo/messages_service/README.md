# Сервис сообщений

Сервис для работы с сообщениями, использующий MongoDB в качестве хранилища данных.

## Запуск

```bash
docker-compose up -d
```

## API

### Аутентификация

Все запросы требуют JWT токена в заголовке `Authorization: Bearer <token>`.

#### Получение токена

```bash
curl -X POST "http://localhost:8000/token" \
  -H "accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"
```

В ответ вы получите JWT токен, который нужно использовать в заголовке `Authorization` для всех последующих запросов.

### Сообщения

#### Создание сообщения

```bash
curl -X POST "http://localhost:8001/messages/create" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"content": "Текст сообщения", "author": 1}'
```

#### Получение сообщения по ID

```bash
curl -X GET "http://localhost:8001/messages/details?message_id=<message_id>" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <token>"
```

#### Обновление сообщения

```bash
curl -X PUT "http://localhost:8001/messages/update?message_id=<message_id>" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"content": "Новый текст сообщения", "author": 1, "id": "<message_id>", "created_at": "<timestamp>", "updated_at": "<timestamp>"}'
```

#### Удаление сообщения

```bash
curl -X DELETE "http://localhost:8001/messages/delete?message_id=<message_id>" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <token>"
```

#### Получение списка сообщений

```bash
# Получить все сообщения
curl -X GET "http://localhost:8001/messages/list" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <token>"

# Получить сообщения конкретного автора
curl -X GET "http://localhost:8001/messages/list?author_id=1" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <token>"

# Получить сообщения с пагинацией
curl -X GET "http://localhost:8001/messages/list?limit=10&offset=0" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <token>"
```

#### Поиск сообщений по тексту

```bash
curl -X GET "http://localhost:8001/messages/search?query=текст" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <token>"
```

## Структура данных

Сообщения хранятся в MongoDB в следующем формате:

```json
{
    "_id": ObjectId(...),
    "value": "текст сообщения",
    "author": число,
    "created_at": дата,
    "updated_at": дата
}
```

## Зависимости

- FastAPI
- Pymongo
- Python-Jose (JWT токены)
- Uvicorn (ASGI сервер) 