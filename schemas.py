from pydantic import BaseModel

# 유저 생성 요청 스키마
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

# 유저 로그인 요청 스키마
class UserLogin(BaseModel):
    email: str
    password: str

# 유저 응답 스키마 (DB 조회 시 사용)
class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True  # ✅ Pydantic V2에서 'orm_mode = True' → 'from_attributes = True'로 변경

