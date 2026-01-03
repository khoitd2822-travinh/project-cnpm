from infrastructure.Model.users_model import Role, UserConferenceRole
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="UTH-ConfMS API")

# Cho phép Frontend React truy cập vào Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dữ liệu giả lập (Thay cho Postgres)
USERS = {
    "admin": {"password": "123", "role": "Chair", "name": "Quản trị viên UTH"},
    "author": {"password": "123", "role": "Author", "name": "Tác giả bài báo"},
}

class LoginSchema(BaseModel):
    username: str
    password: str

@app.post("/api/login")
async def login(data: LoginSchema):
    user = USERS.get(data.username)
    if user and user["password"] == data.password:
        return {
            "status": "success",
            "token": "fake-jwt-token-auth",
            "user": {"username": data.username, "role": user["role"], "name": user["name"]}
        }
    raise HTTPException(status_code=401, detail="Sai tài khoản hoặc mật khẩu")



#
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
#