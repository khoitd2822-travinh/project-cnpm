-- =============================
-- RESET DATABASE (DEV ONLY)
-- =============================
DROP TABLE IF EXISTS user_conference_roles CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

-- =============================
-- 1. TABLE: roles
-- =============================
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO roles (role_name)
VALUES 
    ('admin'),
    ('chair'),
    ('reviewer'),
    ('author');

-- =============================
-- 2. TABLE: users (CHUẨN LOGIN / REGISTER)
-- =============================
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'author'
);

-- =============================
-- 3. TABLE: user_conference_roles
-- =============================
CREATE TABLE user_conference_roles (
    user_id INT NOT NULL,
    conf_id INT NOT NULL,
    role_id INT NOT NULL,

    PRIMARY KEY (user_id, conf_id, role_id),

    CONSTRAINT fk_ucr_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_ucr_role
        FOREIGN KEY (role_id)
        REFERENCES roles(role_id)
        ON DELETE CASCADE
);

-- =============================
-- 4. TABLE: audit_logs (BẢNG CÒN THIẾU)
-- =============================
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_audit_user 
        FOREIGN KEY (user_id) 
        REFERENCES users(user_id) 
        ON DELETE SET NULL
);
-- =============================
-- DONE
-- Tạo bảng hội nghị
CREATE TABLE IF NOT EXISTS conferences (
    conf_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'upcoming' -- 'upcoming', 'ongoing', 'finished'
);

-- Tạo bảng bài báo (papers)
CREATE TABLE IF NOT EXISTS papers (
    paper_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    status TEXT DEFAULT 'Pending' -- Trạng thái: Chờ duyệt, Đã duyệt, v.v.
);
-- =============================
ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
-- Xóa toàn bộ dữ liệu trong bảng users để đăng ký lại từ đầu
TRUNCATE TABLE users RESTART IDENTITY CASCADE;