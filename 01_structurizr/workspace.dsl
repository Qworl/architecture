workspace {
    name "Мессенджер"
    !identifiers hierarchical

    model {
        user = Person "Пользователь"

        messengerSystem = softwareSystem "Мессенджер" {
            description "Система обмена сообщениями между пользователями"

            webApp = container "Веб-приложение" {
                description "Предоставляет функциональность мессенджера через веб-интерфейс"
                technology "React"
                tags "frontend"
            }

            mobileApp = container "Мобильное приложение" {
                description "Предоставляет функциональность мессенджера через мобильное приложение"
                technology "React Native"
                tags "frontend"
            }

            apiGateway = container "API Gateway" {
                description "Единая точка входа для всех клиентских запросов"
                technology "Go"
                tags "backend"
            }

            userService = container "Сервис пользователей" {
                description "Управляет пользователями и их профилями"
                technology "Go"
                tags "backend"

                userComponent = component "Компонент управления пользователями" {
                    description "Обрабатывает создание, поиск и управление пользователями"
                    technology "Go"
                }

                userSearchComponent = component "Компонент поиска пользователей" {
                    description "Обрабатывает быстрый поиск пользователей по логину и маске имени/фамилии"
                    technology "Go"
                }

                userDatabase = component "База данных пользователей" {
                    description "Хранит информацию о пользователях"
                    technology "PostgreSQL"
                    tags "database"
                }
                
                elasticSearch = component "ElasticSearch" {
                    description "Индексирует данные пользователей для быстрого поиска"
                    technology "ElasticSearch"
                    tags "search"
                }
                
                userComponent -> userDatabase "Читает и записывает данные пользователей"
                userComponent -> elasticSearch "Индексирует данные пользователей"
                userSearchComponent -> elasticSearch "Выполняет быстрый поиск"
            }

            chatService = container "Сервис чатов" {
                description "Управляет групповыми чатами и их участниками"
                technology "Go"
                tags "backend"

                groupChatComponent = component "Компонент групповых чатов" {
                    description "Обрабатывает создание групповых чатов и управление участниками"
                    technology "Go"
                }

                chatDatabase = component "База данных чатов" {
                    description "Хранит информацию о групповых чатах и их участниках"
                    technology "PostgreSQL"
                    tags "database"
                }
            }

            messageService = container "Сервис сообщений" {
                description "Управляет сообщениями в групповых и PtP чатах"
                technology "Go"
                tags "backend"

                messageProcessingComponent = component "Компонент обработки сообщений" {
                    description "Обрабатывает отправку и получение сообщений для всех типов чатов"
                    technology "Go"
                }

                messageDatabase = component "База данных сообщений" {
                    description "Хранит сообщения групповых и PtP чатов"
                    technology "PostgreSQL"
                    tags "database"
                }

                unreadMessagesCache = component "Кэш непрочитанных сообщений" {
                    description "Хранит информацию о непрочитанных сообщениях для быстрого доступа"
                    technology "Redis"
                    tags "cache"
                }
                
                messageStatusComponent = component "Компонент статуса сообщений" {
                    description "Отслеживает статус прочтения сообщений"
                    technology "Go"
                }
                
                kafkaProducerComponent = component "Kafka Producer" {
                    description "Публикует события о новых сообщениях"
                    technology "Apache Kafka"
                    tags "messaging"
                }
                
                mediaStorageComponent = component "Компонент хранения медиа" {
                    description "Управляет загрузкой и хранением фото и видео"
                    technology "Go/S3"
                }
                
                mediaProcessingComponent = component "Компонент обработки медиа" {
                    description "Обрабатывает загруженные медиафайлы (сжатие, конвертация)"
                    technology "Go/FFmpeg"
                }
                
                messageSearchComponent = component "Компонент поиска сообщений" {
                    description "Обеспечивает поиск по содержимому сообщений"
                    technology "Go"
                }
                
                messageElasticSearch = component "ElasticSearch сообщений" {
                    description "Индексирует содержимое сообщений для быстрого поиска"
                    technology "ElasticSearch"
                    tags "search"
                }
                
                mediaProcessingQueue = component "Очередь обработки медиа" {
                    description "Очередь для асинхронной обработки медиафайлов"
                    technology "RabbitMQ"
                    tags "messaging"
                }
                
                readReceiptComponent = component "Компонент подтверждения прочтения" {
                    description "Обрабатывает подтверждения прочтения сообщений пользователями"
                    technology "Go"
                }
                
                messageProcessingComponent -> messageDatabase "Читает и записывает сообщения"
                messageProcessingComponent -> unreadMessagesCache "Обновляет кэш непрочитанных сообщений"
                messageProcessingComponent -> kafkaProducerComponent "Отправляет события о новых сообщениях"
                messageProcessingComponent -> mediaStorageComponent "Сохраняет прикрепленные медиафайлы"
                messageProcessingComponent -> messageSearchComponent "Отправляет сообщения на индексацию" "Kafka"
                messageStatusComponent -> unreadMessagesCache "Читает и обновляет статусы сообщений"
                messageStatusComponent -> messageDatabase "Обновляет статусы в базе данных"
                mediaStorageComponent -> mediaProcessingQueue "Отправляет задачи на обработку медиа"
                mediaProcessingQueue -> mediaProcessingComponent "Передает задачи на обработку"
                messageSearchComponent -> messageElasticSearch "Индексирует сообщения"
                readReceiptComponent -> messageStatusComponent "Обновляет статусы прочтения"
                readReceiptComponent -> kafkaProducerComponent "Отправляет события о прочтении сообщений"
            }

            notificationService = container "Сервис уведомлений" {
                description "Отправляет уведомления пользователям о новых сообщениях"
                technology "Go"
                tags "backend"
                
                webSocketComponent = component "Компонент WebSocket" {
                    description "Обрабатывает WebSocket соединения для веб-клиентов"
                    technology "Go/WebSocket"
                }
                
                pushNotificationComponent = component "Компонент Push-уведомлений" {
                    description "Отправляет push-уведомления на мобильные устройства"
                    technology "Firebase Cloud Messaging"
                }
                
                notificationQueueComponent = component "Очередь уведомлений" {
                    description "Обрабатывает и распределяет уведомления"
                    technology "RabbitMQ"
                }
                
                deviceRegistryComponent = component "Реестр устройств" {
                    description "Хранит информацию о подключенных устройствах пользователей"
                    technology "Redis"
                }
                
                kafkaComponent = component "Kafka Consumer" {
                    description "Получает события о новых сообщениях"
                    technology "Apache Kafka"
                    tags "messaging"
                }
                
                notificationQueueComponent -> webSocketComponent "Отправляет уведомления для веб-клиентов"
                notificationQueueComponent -> pushNotificationComponent "Отправляет уведомления для мобильных клиентов"
                webSocketComponent -> deviceRegistryComponent "Проверяет активные соединения"
                pushNotificationComponent -> deviceRegistryComponent "Получает токены устройств"
                kafkaComponent -> notificationQueueComponent "Передает события для обработки"
            }

            // Связи между контейнерами
            webApp -> apiGateway "Отправляет запросы" "JSON/HTTPS"
            mobileApp -> apiGateway "Отправляет запросы" "JSON/HTTPS"
            
            apiGateway -> userService "Перенаправляет запросы" "JSON/HTTPS"
            apiGateway -> chatService "Перенаправляет запросы" "JSON/HTTPS"
            apiGateway -> messageService "Перенаправляет запросы" "JSON/HTTPS"
            
            chatService -> userService "Проверяет существование пользователей" "JSON/HTTPS"
            messageService -> chatService "Проверяет существование чатов" "JSON/HTTPS"
            messageService -> userService "Проверяет существование пользователей" "JSON/HTTPS"
            
            messageService -> notificationService "Отправляет события о новых сообщениях" "Kafka"
            
            notificationService -> webApp "Доставляет сообщения в реальном времени" "WebSocket"
            notificationService -> mobileApp "Доставляет push-уведомления" "FCM"
            
            messageService -> messageService "Внутренние операции (загрузка сообщений, обновление статусов)" "Internal"
            
            chatService -> chatService "Внутренние операции (добавление пользователей в чат)" "Internal"
            
            // Связи между компонентами
            chatService.groupChatComponent -> chatService.chatDatabase "Читает и записывает данные чатов"

            notificationService -> userService "Получает информацию об устройствах пользователей" "JSON/HTTPS"
            notificationService.notificationQueueComponent -> userService "Получает информацию о пользователях" "JSON/HTTPS"

            apiGateway -> messageService.unreadMessagesCache "Быстрое получение непрочитанных сообщений" "Redis"
            apiGateway -> messageService.messageSearchComponent "Поиск по сообщениям" "JSON/HTTPS"
            apiGateway -> messageService.readReceiptComponent "Отправляет подтверждения прочтения" "JSON/HTTPS"
            apiGateway -> messageService.messageProcessingComponent "Отправляет запросы на обработку сообщений" "JSON/HTTPS"
        }

        user -> messengerSystem.webApp "Использует"
        user -> messengerSystem.mobileApp "Использует"

        deploymentEnvironment "Production" {
            deploymentNode "Инфраструктура клиента" {
                deploymentNode "Веб-браузер" {
                    clientWebApp = containerInstance messengerSystem.webApp
                }
                
                deploymentNode "Мобильное устройство" {
                    clientMobileApp = containerInstance messengerSystem.mobileApp
                }
            }
            
            deploymentNode "Облачная инфраструктура" {
                deploymentNode "API Gateway Cluster" {
                    gatewayInstance = containerInstance messengerSystem.apiGateway
                    instances 2
                }
                
                deploymentNode "Сервисный кластер" {
                    userServiceInstance = containerInstance messengerSystem.userService
                    chatServiceInstance = containerInstance messengerSystem.chatService
                    messageServiceInstance = containerInstance messengerSystem.messageService
                    notificationServiceInstance = containerInstance messengerSystem.notificationService
                    instances 2
                }
                
                deploymentNode "Кластер баз данных" {
                    dbNode = infrastructureNode "PostgreSQL Cluster" {
                        description "Кластер баз данных PostgreSQL с репликацией"
                        technology "PostgreSQL"
                    }
                }
            }
        }
    }

    views {
        themes default
        
        systemContext messengerSystem "SystemContext" {
            include *
            autoLayout
        }
        
        container messengerSystem "Containers" {
            include *
            autoLayout
        }
        
        component messengerSystem.userService "UserServiceComponents" {
            include *
            autoLayout
        }
        
        component messengerSystem.chatService "ChatServiceComponents" {
            include *
            autoLayout
        }
        
        component messengerSystem.messageService "MessageServiceComponents" {
            include *
            autoLayout
        }

        component messengerSystem.notificationService "NotificationServiceComponents" {
            include *
            autoLayout
        }
        
        deployment messengerSystem "Production" {
            include *
            autoLayout
        }
        
        dynamic messengerSystem "UC1_CreateUser" "Создание нового пользователя" {
            user -> messengerSystem.webApp "Отправляет данные для регистрации"
            messengerSystem.webApp -> messengerSystem.apiGateway "POST /api/users"
            messengerSystem.apiGateway -> messengerSystem.userService "Создает пользователя"
            autoLayout lr
        }
        
        dynamic messengerSystem "UC2_SearchUser" "Поиск пользователя" {
            user -> messengerSystem.webApp "Вводит критерии поиска"
            messengerSystem.webApp -> messengerSystem.apiGateway "GET /api/users?query=..."
            messengerSystem.apiGateway -> messengerSystem.userService "Поиск пользователя"
            autoLayout lr
        }
        
        dynamic messengerSystem "UC3_CreateGroupChat" "Создание группового чата" {
            user -> messengerSystem.webApp "Создает групповой чат"
            messengerSystem.webApp -> messengerSystem.apiGateway "POST /api/chats"
            messengerSystem.apiGateway -> messengerSystem.chatService "Перенаправляет запрос"
            messengerSystem.chatService -> messengerSystem.userService "Проверяет пользователей"
            autoLayout lr
        }
    
        
        dynamic messengerSystem "UC4_SendPtPMessage" "Отправка PtP сообщения" {
            user -> messengerSystem.webApp "Отправляет личное сообщение"
            messengerSystem.webApp -> messengerSystem.apiGateway "POST /api/messages/direct"
            messengerSystem.apiGateway -> messengerSystem.messageService "Перенаправляет запрос"
            messengerSystem.messageService -> messengerSystem.userService "Проверяет существование пользователя"
            messengerSystem.messageService -> messengerSystem.notificationService "Отправляет уведомление"
            autoLayout lr
        }

        dynamic messengerSystem "UC5_MessageDelivery" "Доставка сообщения всем пользователям чата" {
            user -> messengerSystem.webApp "Отправляет сообщение в групповой чат"
            messengerSystem.webApp -> messengerSystem.apiGateway "POST /api/chats/{id}/messages"
            messengerSystem.apiGateway -> messengerSystem.messageService "Перенаправляет запрос"
            messengerSystem.messageService -> messengerSystem.chatService "Получает список участников чата"
            messengerSystem.messageService -> messengerSystem.notificationService "Отправляет событие о новом сообщении"
            messengerSystem.notificationService -> messengerSystem.userService "Получает информацию об устройствах пользователей"
            messengerSystem.notificationService -> messengerSystem.webApp "Доставляет сообщение в реальном времени"
            messengerSystem.notificationService -> messengerSystem.mobileApp "Доставляет push-уведомление"
            autoLayout lr
        }

        dynamic messengerSystem "UC6_UploadMedia" "Загрузка медиафайла в чат" {
            user -> messengerSystem.webApp "Загружает фото/видео"
            messengerSystem.webApp -> messengerSystem.apiGateway "POST /api/messages/{id}/media"
            messengerSystem.apiGateway -> messengerSystem.messageService "Перенаправляет запрос"
            messengerSystem.messageService -> messengerSystem.messageService "Сохраняет медиафайл"
            messengerSystem.messageService -> messengerSystem.notificationService "Отправляет уведомление"
            autoLayout lr
        }

        dynamic messengerSystem "UC7_SearchMessages" "Поиск по сообщениям" {
            user -> messengerSystem.webApp "Вводит поисковый запрос"
            messengerSystem.webApp -> messengerSystem.apiGateway "GET /api/messages/search?query=..."
            messengerSystem.apiGateway -> messengerSystem.messageService "Перенаправляет запрос"
            messengerSystem.messageService -> messengerSystem.messageService "Выполняет поиск по сообщениям"
            autoLayout lr
        }

        dynamic messengerSystem "UC8_GetChatMessages" "Получение сообщений чата" {
            user -> messengerSystem.webApp "Открывает чат"
            messengerSystem.webApp -> messengerSystem.apiGateway "GET /api/chats/{id}/messages"
            messengerSystem.apiGateway -> messengerSystem.messageService "Перенаправляет запрос"
            messengerSystem.messageService -> messengerSystem.chatService "Проверяет права доступа к чату"
            messengerSystem.messageService -> messengerSystem.messageService "Загружает сообщения"
            messengerSystem.messageService -> messengerSystem.messageService "Обновляет статусы прочтения"
            autoLayout lr
        }

        dynamic messengerSystem "UC9_MarkMessageAsRead" "Отметка сообщения как прочитанного" {
            user -> messengerSystem.webApp "Просматривает сообщение"
            messengerSystem.webApp -> messengerSystem.apiGateway "POST /api/messages/{id}/read"
            messengerSystem.apiGateway -> messengerSystem.messageService "Перенаправляет запрос"
            messengerSystem.messageService -> messengerSystem.messageService "Обрабатывает подтверждение прочтения"
            messengerSystem.messageService -> messengerSystem.messageService "Обновляет статус в базе данных и кэше"
            autoLayout lr
        }

        dynamic messengerSystem "UC10_AddUserToChat" "Добавление пользователя в чат" {
            user -> messengerSystem.webApp "Добавляет пользователя в чат"
            messengerSystem.webApp -> messengerSystem.apiGateway "POST /api/chats/{id}/users"
            messengerSystem.apiGateway -> messengerSystem.chatService "Перенаправляет запрос"
            messengerSystem.chatService -> messengerSystem.userService "Проверяет существование пользователя"
            messengerSystem.chatService -> messengerSystem.chatService "Добавляет пользователя в чат"
            autoLayout lr
        }

        dynamic messengerSystem "UC11_GetPtPMessages" "Получение списка личных сообщений" {
            user -> messengerSystem.webApp "Открывает личный чат"
            messengerSystem.webApp -> messengerSystem.apiGateway "GET /api/messages/direct/{userId}"
            messengerSystem.apiGateway -> messengerSystem.messageService "Перенаправляет запрос"
            messengerSystem.messageService -> messengerSystem.userService "Проверяет существование пользователя"
            messengerSystem.messageService -> messengerSystem.messageService "Загружает личные сообщения"
            messengerSystem.messageService -> messengerSystem.messageService "Обновляет статусы прочтения"
            autoLayout lr
        }
    }
}