from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text 
import uvicorn

from infrastructure.databases.postgresql import SessionLocal
# Chú ý: admin_router phải được định nghĩa trong src/admin_endpoints.py
from src.admin_endpoints import admin_router

app = FastAPI()

# CORS mở hoàn toàn để React không bị chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router, prefix="/api")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RegisterSchema(BaseModel):
    full_name: str
    email: str
    password: str
    role: str

class LoginSchema(BaseModel):
    username: str
    password: str

@app.post("/api/register")
async def register(data: RegisterSchema, db: Session = Depends(get_db)):
    try:
        query = text("""
            INSERT INTO users (full_name, username, email, password, role) 
            VALUES (:fn, :un, :em, :pw, :rl)
        """)
        db.execute(query, {
            "fn": data.full_name, "un": data.email, "em": data.email,
            "pw": data.password, "rl": data.role
        })
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/login")
async def login(data: LoginSchema, db: Session = Depends(get_db)):
    query = text("SELECT full_name, role, password FROM users WHERE email = :em")
    user = db.execute(query, {"em": data.username}).fetchone()
    if user and user[2] == data.password:
        return {
            "status": "success",
            "token": "secret-token",
            "user": {"name": user[0], "role": user[1]}
        }
    raise HTTPException(status_code=401, detail="Sai tài khoản hoặc mật khẩu")

if __name__ == "__main__":
    # CHẠY TRÊN CỔNG 5000 KHỚP VỚI MÔI TRƯỜNG CỦA BẠN
    uvicorn.run(app, host="127.0.0.1", port=5000)