from sqlalchemy import Column, Integer, String
from database import Base, engine

# User 테이블 정의
class User(Base):
    __tablename__ = "users"  # MySQL 테이블 이름

    id = Column(Integer, primary_key=True, index=True)  # 기본 키 (PK)
    email = Column(String(100), unique=True, nullable=False)  # 이메일 (고유값)
    password = Column(String(255), nullable=False)  # 해시된 비밀번호 저장
    name = Column(String(50), nullable=False)  # 유저 이름

# ✅ 테이블 강제 생성 (이 코드가 있어야 테이블이 만들어짐)
Base.metadata.create_all(bind=engine)


