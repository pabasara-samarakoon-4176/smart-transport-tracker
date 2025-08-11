-- 1. Create the database (run as a superuser or postgres user)
CREATE DATABASE user_service_db;

-- Then connect to the database, e.g., \c user_service_db in psql

-- 2. Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
