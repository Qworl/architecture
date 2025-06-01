# Команды для работы с сервисом

* Получить токен - `curl -X POST "http://0.0.0.0:8000/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=secret"`

* Вывести всех пользователей - `curl -X GET "http://0.0.0.0:8000/users/list" -H "accept: application/json" -H "Authorization: Bearer <token>"`

* Детали пользователя - `curl -X GET "http://0.0.0.0:8000/users/details?user_id=5" -H "accept: application/json" -H "Authorization: Bearer <token>"`

* Поиск по логину - `curl -X GET "http://0.0.0.0:8000/users/list?login=admin" -H "accept: application/json" -H "Authorization: Bearer <token>`

Поиск по имени - `curl -X GET "http://0.0.0.0:8000/users/list?name=Test" -H "accept: application/json" -H "Authorization: Bearer <token>`

* Поиск по имени и фамилии - `curl -X GET "http://0.0.0.0:8000/users/list?name=Test&surname=User1" -H "accept: application/json" -H "Authorization: Bearer <token>`

* Создать пользователя - `curl -X POST "http://0.0.0.0:8000/users/create" -H "accept: application/json" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"username":"admin1","email":"admin@example.ru","password":"secret","name":"Admin","surname":"Admin","age":30}'`

* Изменить пользователя - `curl -X PUT "http://0.0.0.0:8000/users/update?user_id=5" -H "accept: application/json" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"username":"admin1","email":"admin@example.ru","password":"secret","name":"Admin","surname":"AdminCorrected","age":30}'`

* Удалить пользователя - `curl -X DELETE "http://0.0.0.0:8000/users/delete?user_id=5" -H "accept: application/json" -H "Authorization: Bearer <token>"`

# Тестирование производительности с Redis и без Redis

## Результаты тестирования

### Endpoint `/users/list`

#### С Redis
| Конфигурация | Requests/sec | Latency (avg) | Throughput |
|--------------|--------------|---------------|------------|
| 1 thread, 1 conn | 362.57 | 2.76ms | 151.54KB/s |
| 5 threads, 5 conn | 392.55 | 12.76ms | 164.08KB/s |
| 10 threads, 10 conn | 356.65 | 28.03ms | 149.07KB/s |

#### Без Redis
| Конфигурация | Requests/sec | Latency (avg) | Throughput |
|--------------|--------------|---------------|------------|
| 1 thread, 1 conn | 324.16 | 3.08ms | 135.49KB/s |
| 5 threads, 5 conn | 335.05 | 14.97ms | 140.04KB/s |
| 10 threads, 10 conn | 217.36 | 45.84ms | 90.85KB/s |

### Endpoint `/users/details`

#### С Redis
| Конфигурация | Requests/sec | Latency (avg) | Throughput |
|--------------|--------------|---------------|------------|
| 1 thread, 1 conn | 388.93 | 2.57ms | 83.95KB/s |
| 5 threads, 5 conn | 429.84 | 11.64ms | 92.77KB/s |
| 10 threads, 10 conn | 256.91 | 38.73ms | 55.45KB/s |

#### Без Redis
| Конфигурация | Requests/sec | Latency (avg) | Throughput |
|--------------|--------------|---------------|------------|
| 1 thread, 1 conn | 331.33 | 3.02ms | 71.51KB/s |
| 5 threads, 5 conn | 350.21 | 14.29ms | 75.58KB/s |
| 10 threads, 10 conn | 226.18 | 44.02ms | 48.81KB/s |

## Анализ результатов

### Улучшение производительности с Redis

1. **Endpoint `/users/list`**:
   - При 1 потоке: +11.8% к requests/sec
   - При 5 потоках: +17.2% к requests/sec
   - При 10 потоках: +64.1% к requests/sec

2. **Endpoint `/users/details`**:
   - При 1 потоке: +17.4% к requests/sec
   - При 5 потоках: +22.7% к requests/sec
   - При 10 потоках: +13.6% к requests/sec

### Наблюдения

1. Redis показывает наибольшее улучшение производительности при высокой нагрузке (10 потоков)
2. Оптимальная конфигурация для обоих эндпоинтов - 5 потоков и соединений
3. Latency значительно ниже при использовании Redis, особенно при высокой нагрузке
4. Throughput (пропускная способность) также выше при использовании Redis

### Выводы

1. Использование Redis значительно улучшает производительность системы
2. Наибольший выигрыш наблюдается при высокой нагрузке
3. Redis особенно эффективен для кэширования детальной информации о пользователях
4. Оптимальное количество потоков/соединений - 5, дальнейшее увеличение может привести к деградации производительности 