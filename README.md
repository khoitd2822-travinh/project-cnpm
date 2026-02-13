# Project-CNPM
```
├── 📂 Backend/                 # Mã nguồn xử lý phía Server
│   ├── 📂 src/                             
│   │   ├── api/
│   │   │   ├── controllers/
│   │   │   │   └── 📄 auth_controller.py
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 auth_api.py 
│   │   ├── domain/ 
│   │   │   └── 📄 user.py
│   │   ├── infrastructure/
│   │   │   ├── databases/ 
│   │   │   │   ├── 📄 __init__.py
│   │   │   │   ├── 📄 base.py
│   │   │   │   ├── 📄 postgresql.py
│   │   │   │   └── 📄 seed_data.sql
│   │   │   ├── Model/ 
│   │   │   │   ├── 📄 assignment_model.py
│   │   │   │   ├── 📄 audilog_model.py
│   │   │   │   ├── 📄 cameraready_model.py
│   │   │   │   ├── 📄 conference_model.py
│   │   │   │   ├── 📄 decision_model.py
│   │   │   │   ├── 📄 paper_model.py
│   │   │   │   ├── 📄 review_model.py
│   │   │   │   ├── 📄 track_model.py  
│   │   │   │   └── 📄 user_model.py
│   │   │   ├── persistence/
│   │   │   │   ├── 📄 audit_repository.py
│   │   │   │   ├── 📄 paper_repository.py
│   │   │   │   ├── 📄 reviewer_repository.py
│   │   │   │   └── 📄 user_repository.py
│   │   │   └── 📄 __init__.py
│   │   ├── services/
│   │   │   ├── application
│   │   │   │   ├── use_cases 
│   │   │   │   └── 📄 assign_paper_use_case.py
│   │   │   ├── entities/
│   │   │   │   ├── 📄 paper.py
│   │   │   │   └── 📄 reviewer.py
│   │   │   ├── interface
│   │   │   │   ├── controller
│   │   │   │   └── 📄 paper_controller.py
│   │   │   ├── repository/
│   │   │   │   ├── 📄 paper_repository.py
│   │   │   │   └── 📄 reviewer_repository.py
│   │   │   ├── 📄 auth_service.py
│   │   │   ├── 📄 author_routes.py
│   │   ├── 📄 admin_endpoints.py        
│   │   ├── 📄 admin_service.py
│   │   ├── 📄 __init__.py
│   │   ├── 📄 app.py
│   │   ├── 📄 config.py
│   │   ├── 📄 main.py
│   │   └──  📄 models.py 
│   └── 📄 assign_paper.py                 
├── 📂 Frontend/                # Mã nguồn giao diện người dùng
│   └── 📂 web-app/             # Dự án chính của Frontend
│   │   ├── 📂 public/          # Chứa các file tĩnh (ảnh, icon)
│   │   ├── 📂 src/
│   │   │   ├── 📄 AdminDashboard.js
│   │   │   ├── 📄 App.css
│   │   │   ├── 📄 App.js
│   │   │   ├── 📄 AuthorDashboard.js
│   │   │   ├── 📄 ChairDashboard.js
│   │   │   ├── 📄 index.css
│   │   │   ├── 📄 index.js
│   │   │   └── 📄 ReviewerDashboard.js
│   │   └── 📄 package.json     # Quản lý thư viện của Frontend
├── 📄 .gitignore               # Chỉ định các file/thư mục không đưa lên GitHub
├── 📄 README.md                # Tài liệu hướng dẫn sử dụng dự án
└── 📄 requirements.txt         # Danh sách thư viện Python cần cài đặt
```
# Download source code (CMD)
    git clone https://github.com/khoitd2822-travinh/project-cnpm.git

# Kiểm tra cài đặt python chưa
    python --version

# Run app : Chạy Backend.
## Bước 1 : Tạo môi trường ảo Python
# Windows :
  	py -m venv .venv

# Unix/MacOS : 
   	python3 -m venv .venv

## Bước 2 : Kích hoạt môi trường ảo ( Window )
    .\Backend\.venv\Scripts\activate

## Bước 3 : Di chuyển đến thư mục và chạy Backend, lần lượt từng dòng ( Window )
    cd Backend/src
    python app.py
## Chạy thành công Backend, mở thêm cửa sổ terminal chạy Frontend ( Backend chạy song song cùng Frontend )
# Chạy Frontend.
## Bước 4 : Di chuyển thư mục và cài đặt thư viện ( chạy từng dòng ) 
    cd Frontend/web-app
    npm install
## Bước 5 : Khởi chạy giao diện 
    npm start

