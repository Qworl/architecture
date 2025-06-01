DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'users') THEN
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            name VARCHAR(50) NOT NULL,
            surname VARCHAR(50) NOT NULL,
            age INTEGER,
            hashed_password VARCHAR(100) NOT NULL
        );

        CREATE INDEX idx_username ON users(username);
        CREATE INDEX idx_email ON users(email);
        CREATE INDEX idx_name_surname ON users(name, surname);

        INSERT INTO users (username, email, name, surname, age, hashed_password)
        VALUES 
            ('admin', 'admin@example.com', 'Admin', 'Admin', 0, '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'),  -- password: secret
            ('test_user1', 'test1@example.com', 'Test', 'User1', 25, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewE.yUZFyGR6POv.'),  -- password: password1
            ('test_user2', 'test2@example.com', 'Test', 'User2', 30, '$2b$12$BHZsX3.KkqsXm9/RzytGj.a.9qx/RG5I/h.1inhZ.e6QBuoL0wAai');  -- password: password2
    END IF;
END
$$; 