# project-CNPM

```text
├── 📂 Backend/                 # Mã nguồn xử lý phía Server
│   └── 📂 src/
│       ├── 📂 api/
│       │   ├── 📂 controllers/
│       │   │   └── 📄 auth_controller.py
│       │   ├── 📄 __init__.py
│       │   └── 📄 auth_api.py
│       ├── 📂 domain/
│       │   └── 📄 user.py
│       ├── 📂 infrastructure/
│       │   ├── 📂 databases/
│       │   │   ├── 📄 base.py
│       │   │   ├── 📄 postgresql.py
│       │   │   └── 📄 seed_data.sql
│       │   ├── 📂 Model/
│       │   │   ├── 📄 assignment_model.py
│       │   │   ├── 📄 user_model.py
│       │   │   └── 📄 ... (các model khác)
│       │   └── 📂 persistence/
│       │       ├── 📄 user_repository.py
│       │       └── 📄 ... (các repository khác)
│       ├── 📂 services/
│       │   ├── 📂 application/use_cases/
│       │   │   └── 📄 assign_paper_use_case.py
│       │   ├── 📂 entities/
│       │   │   ├── 📄 paper.py
│       │   │   └── 📄 reviewer.py
│       │   ├── 📂 interface/controller/
│       │   │   └── 📄 paper_controller.py
│       │   ├── 📂 repository/
│       │   ├── 📄 auth_service.py
│       │   └── 📄 author_routes.py
│       ├── 📄 app.py
│       ├── 📄 config.py
│       ├── 📄 main.py
│       └── 📄 models.py
├── 📂 Frontend/web-app/        # Mã nguồn giao diện người dùng
│   ├── 📂 public/              # File tĩnh (ảnh, icon)
│   ├── 📂 src/
│   │   ├── 📄 AdminDashboard.js
│   │   ├── 📄 AuthorDashboard.js
│   │   ├── 📄 App.js
│   │   └── 📄 index.js
│   └── 📄 package.json         # Quản lý thư viện Frontend
├── 📄 .gitignore               # Cấu hình loại bỏ file rác
└── 📄 requirements.txt         # Danh sách thư viện Python
