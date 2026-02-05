
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from infrastructure.databases.postgresql import init_postgresql, SessionLocal
from werkzeug.security import generate_password_hash, check_password_hash

import uvicorn

app = FastAPI()

# CORS mở hoàn toàn để React không bị chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            "pw": generate_password_hash(data.password), "rl": data.role
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
    if user and check_password_hash(user[2], data.password):
        return {
            "status": "success",
            "token": "secret-token",
            "user": {"name": user[0], "role": user[1]}
        }
    raise HTTPException(status_code=401, detail="Sai tài khoản hoặc mật khẩu")


@app.get("/")
def root():
    return {"message": "Backend is running"}

if __name__ == "__main__":
    print("--- ĐANG TỰ ĐỘNG TẠO BẢNG DATABASE ---")
    init_postgresql()
    print("--- DATABASE ĐÃ SẴN SÀNG ---")
    print("FastAPI running on http://127.0.0.1:5001")
    uvicorn.run(app, host="127.0.0.1", port=5001, debug=True)
