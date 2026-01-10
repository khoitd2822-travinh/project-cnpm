
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'author',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- 1. Tạo bảng roles
CREATE TABLE IF NOT EXISTS roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS user_conference_roles (
    user_id INT NOT NULL,
    conf_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, conf_id, role_id)
);

INSERT INTO roles (role_name) VALUES ('admin'), ('chair'), ('reviewer'), ('author') 
ON CONFLICT (role_name) DO NOTHING;

INSERT INTO user_conference_roles (user_id, conf_id, role_id) 
VALUES (1, 1, (SELECT role_id FROM roles WHERE role_name = 'reviewer'))
ON CONFLICT DO NOTHING;

ALTER USER postgres WITH PASSWORD '1234';
DROP TABLE IF EXISTS users CASCADE;



