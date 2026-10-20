# src/database/models.py
from sqlalchemy import (Integer, String, Boolean, DateTime, func, Table,
                        Column, ForeignKey)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
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
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )
    
    users: Mapped[List["User"]] = relationship(
        secondary=users_skills,
        back_populates="skills",
    )
    exchanges: Mapped[List["Exchange"]] = relationship(back_populates="skill")
    
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    bio: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")

    skills: Mapped[List[Skill]] = relationship(
        secondary=users_skills,
        back_populates="users",
    )
    sent_exchanges: Mapped[List["Exchange"]] = relationship(
        foreign_keys="Exchange.sender_id",
        back_populates="sender",
    )
    received_exchanges: Mapped[List["Exchange"]] = relationship(
        foreign_keys="Exchange.receiver_id",
        back_populates="receiver",
    )
    reviews_given: Mapped[List["Review"]] = relationship(
        foreign_keys="Review.reviewer_id",
        back_populates="reviewer",
    )
    reviews_received: Mapped[List["Review"]] = relationship(
        foreign_keys="Review.reviewed_id",
        back_populates="reviewed",
    )

class Exchange(Base):
    __tablename__ = "exchanges"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    message: Mapped[str | None] = mapped_column(String(250), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        server_default="pending",
        nullable=False,
    )
    hours_proposed: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),
                                                 onupdate=func.now())
    
    skill: Mapped["Skill"] = relationship(back_populates="exchanges")
    sender: Mapped["User"] = relationship(
        foreign_keys=[sender_id],
        back_populates="sent_exchanges",
    )
    receiver: Mapped["User"] = relationship(
        foreign_keys=[receiver_id],
        back_populates="received_exchanges",
    )
    reviews: Mapped[List["Review"]] = relationship(
        back_populates="exchange",
    )
    
class Review(Base):
    __tablename__ = "reviews"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_id: Mapped[int] = mapped_column(
        ForeignKey("exchanges.id"),
        unique=True,
        nullable=False,
    )
    reviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    reviewed_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    exchange: Mapped["Exchange"] = relationship(
        foreign_keys=[exchange_id],
        back_populates="reviews",
    )
    reviewer: Mapped["User"] = relationship(
        foreign_keys=[reviewer_id],
        back_populates="reviews_given",
    )
    reviewed: Mapped["User"] = relationship(
        foreign_keys=[reviewed_id],
        back_populates="reviews_received",
    )
    
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str | None] = mapped_column(String(250), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
