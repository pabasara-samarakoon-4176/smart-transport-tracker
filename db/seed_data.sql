INSERT INTO routes (name, origin, destination) VALUES
('Route A', 'Colombo Fort', 'Battaramulla'),
('Route B', 'Galle', 'Matara');

INSERT INTO buses (registration_no, route_id) VALUES
('WP-NA-2245', 1),
('CP-KQ-3482', 2);

INSERT INTO users (name, phone, firebase_uid) VALUES
('John Doe', '+94770000000', 'firebase_john_001');