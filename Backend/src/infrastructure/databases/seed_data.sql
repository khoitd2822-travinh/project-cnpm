DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS papers CASCADE;
DROP TABLE IF EXISTS user_conference_roles CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ==========================================
-- 2. TẠO CÁC BẢNG MỚI
-- ==========================================

-- Bảng người dùng
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'author',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng bài báo (Quan trọng: Đã có sẵn cột reviewer_id)
-- Bảng bài báo (Quan trọng: Đã có sẵn cột reviewer_id)
CREATE TABLE papers (
    paper_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    abstract TEXT,
    file_path VARCHAR(255),
    author_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    reviewer_id INT REFERENCES users(user_id) ON DELETE SET NULL,
    status VARCHAR(50) DEFAULT 'Đang chờ',
    score FLOAT,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng đánh giá
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    paper_id INT REFERENCES papers(paper_id) ON DELETE CASCADE,
    reviewer_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    score INT CHECK (score >= 1 AND score <= 10),
    comments TEXT,
    status VARCHAR(50) DEFAULT 'Hoàn thành',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng vai trò bổ sung (nếu cần mở rộng)
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

-- ==========================================
-- 3. CHÈN DỮ LIỆU CẤU HÌNH GỐC
-- ==========================================

INSERT INTO roles (role_name) VALUES 
('admin'), ('chair'), ('reviewer'), ('author') 
ON CONFLICT (role_name) DO NOTHING;

-- Thêm cột điểm số (cho phép số lẻ như 7.5, 8.2)
ALTER TABLE papers ADD COLUMN IF NOT EXISTS score FLOAT;


ALTER USER postgres WITH PASSWORD '1234';

-- Xóa sạch dữ liệu trong bảng và reset ID về 

SELECT paper_id, title, author_id, reviewer_id, status FROM papers;
UPDATE papers 
SET reviewer_id = 2  -- Thay 2 bằng ID của reviewer bạn muốn test
WHERE paper_id = 1;  -- Thay 1 bằng paper_id bất kỳ

