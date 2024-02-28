-- user table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL, -- later on figure out hashing this
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(20) CHECK (role IN ('s', 'p'))
);
-- courses table
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    semester VARCHAR(50) NOT NULL,
    UNIQUE(course_name, year, semester) --ensures that the combination is unique across all rows
);
-- intents table
CREATE TABLE intents (
    intent_id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    course_id INT,-- does not need to be 'not NULL' 
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL
);
-- documents table
CREATE TABLE documents (
    document_id SERIAL PRIMARY KEY,
    document_data JSONB NOT NULL,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);
-- chat logs table
CREATE TABLE chat_logs (
    chat_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    message TEXT NOT NULL,
    intent_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (intent_id) REFERENCES intents(intent_id) ON DELETE SET NULL
);