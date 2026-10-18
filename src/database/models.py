# src/database/models.py
from sqlalchemy import (select, Integer, String, create_engine, Boolean, 
                        DateTime, func, Table, Column, ForeignKey)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker, relationship
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    pass

users_skills = Table(
    "user_skills",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True)
)

class Skill(Base):
    __tablename__ = "skills"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[str] = mapped_column(String(100), nullable=False)
    can_teach: Mapped[bool] = mapped_column(Boolean, default=False)
    want_learn: Mapped[bool] = mapped_column(Boolean, default=False)
    
    users: Mapped[List["User"]] = relationship(secondary=users_skills, back_populates="skills")
    
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    bio: Mapped[str] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    skills: Mapped[List[Skill]] = relationship(secondary=users_skills, back_populates="users")
    