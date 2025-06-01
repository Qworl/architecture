db = db.getSiblingDB('messages_db');

db.createCollection('messages');

db.messages.createIndex({ "value": "text" });
db.messages.createIndex({ "author": 1 });

const initialMessages = [
    {
        _id: ObjectId("507f1f77bcf86cd799439011"),
        value: "Привет! Как дела?",
        author: 1,
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        _id: ObjectId("507f1f77bcf86cd799439012"),
        value: "Отлично, спасибо! А у тебя?",
        author: 2,
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        _id: ObjectId("507f1f77bcf86cd799439013"),
        value: "Тоже хорошо. Что нового?",
        author: 1,
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        _id: ObjectId("507f1f77bcf86cd799439014"),
        value: "Работаю над новым проектом с использованием MongoDB",
        author: 2,
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        _id: ObjectId("507f1f77bcf86cd799439015"),
        value: "Интересно! Расскажи подробнее",
        author: 1,
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        _id: ObjectId("507f1f77bcf86cd799439016"),
        value: "Создаю сервис для обмена сообщениями с полнотекстовым поиском",
        author: 2,
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        _id: ObjectId("507f1f77bcf86cd799439017"),
        value: "Звучит здорово! Какие технологии используешь?",
        author: 1,
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        _id: ObjectId("507f1f77bcf86cd799439018"),
        value: "FastAPI, MongoDB, Docker. Все современные инструменты",
        author: 2,
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        _id: ObjectId("507f1f77bcf86cd799439019"),
        value: "Отличный стек! Удачи в разработке",
        author: 1,
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        _id: ObjectId("507f1f77bcf86cd799439020"),
        value: "Спасибо! Буду держать в курсе прогресса",
        author: 2,
        created_at: new Date(),
        updated_at: new Date()
    }
];

db.messages.insertMany(initialMessages);

print("MongoDB initialization completed: messages collection created with initial data");