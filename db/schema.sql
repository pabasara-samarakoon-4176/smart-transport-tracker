-- Create table for buses
CREATE TABLE buses (
    id SERIAL PRIMARY KEY,
    registration_no VARCHAR(20) UNIQUE NOT NULL,
    route_id INT
);

-- Table for routes
CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    origin VARCHAR(50),
    destination VARCHAR(50)
);

-- Real-time locations sent from GPS
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    bus_id INT REFERENCES buses(id),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Users who subscribe to alerts
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20),
    firebase_uid VARCHAR(100)
);

-- Alerts created by users
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    bus_id INT REFERENCES buses(id),
    location_lat DECIMAL(9,6),
    location_lon DECIMAL(9,6),
    radius_m INT, -- Radius in meters
    alert_triggered BOOLEAN DEFAULT FALSE
);