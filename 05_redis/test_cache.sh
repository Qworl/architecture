#!/bin/bash

set -e  # Остановка скрипта при любой ошибке

# Функция для получения токена с таймаутом
get_token() {
    echo "Получение токена..."
    TOKEN=$(timeout 5 curl -s -X POST "http://0.0.0.0:8000/token" \
        -H "accept: application/json" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=admin&password=admin" | jq -r '.access_token')
    
    if [ -z "$TOKEN" ]; then
        echo "Ошибка: Не удалось получить токен"
        exit 1
    fi
    echo "Токен получен успешно"
}

# Создаем директорию для результатов
mkdir -p results

# Функция для запуска теста
run_test() {
    local endpoint=$1
    local threads=$2
    local connections=$2  # Используем то же значение для connections
    
    echo "Запуск теста для $endpoint с $threads потоками и $connections соединениями..."
    
    # Проверяем доступность сервиса перед тестом
    if ! curl -s -f "http://0.0.0.0:8000/users/list" > /dev/null; then
        echo "Ошибка: Сервис недоступен"
        exit 1
    fi
    
    # Запускаем wrk с таймаутом
    timeout 15 wrk -t$threads -c$connections -d5s \
        -H "Authorization: Bearer $TOKEN" \
        "http://0.0.0.0:8000/users/$endpoint" > "results/wrk_${endpoint}_${threads}t_${connections}c.txt" 2>&1
    
    if [ $? -eq 124 ]; then
        echo "Тест прерван по таймауту"
        echo "TIMEOUT" >> "results/wrk_${endpoint}_${threads}t_${connections}c.txt"
    fi
    
    echo "Тест завершен, результаты сохранены в results/wrk_${endpoint}_${threads}t_${connections}c.txt"
}

# Получаем токен
get_token

# Запускаем тесты для /list
echo "Тестирование /list endpoint..."
run_test "list" 1
run_test "list" 5
run_test "list" 10

# Запускаем тесты для /details
echo "Тестирование /details endpoint..."
run_test "details?user_id=1" 1
run_test "details?user_id=1" 5
run_test "details?user_id=1" 10

echo "Все тесты завершены. Результаты доступны в директории results/" 