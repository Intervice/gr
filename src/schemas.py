# src/schemas.py
from pydantic import BaseModel, Field, model_validator, ConfigDict, EmailStr
from enum import Enum
from datetime import datetime
from typing import List

class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"

class SkillCategory(str, Enum):
    programming = "programming"
    music = "music"
    languages = "languages"
    science = "science"
    sport = "sport"

class SkillBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=500)
    category: SkillCategory
    level: SkillLevel
    
class SkillCreate(SkillBase):
    can_teach: bool
    want_learn: bool
    
    @model_validator(mode="after")
    def check_fields(self):
        if self.can_teach == self.want_learn:
            raise ValueError("You can't be teacher and student in single skill or neither.")
        return self
    
class SkillUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, min_length=10, max_length=500)
    category: SkillCategory | None = None
    level: SkillLevel | None = None
    can_teach: bool | None = None
    want_learn: bool | None = None
    
    @model_validator(mode="after")
    def check_teach_learn_fields(self):
        if self.can_teach is not None and self.want_learn is not None:
            if self.can_teach == self.want_learn:
                raise ValueError("You can't be teacher and student in a single skill or neither.")
        return self

class SkillResponse(SkillBase):
    id: int
    can_teach: bool
    want_learn: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    username: str = Field(..., max_length=100)
    email: EmailStr
    bio: str | None = Field(None, max_length=1000)
    is_active: bool = True

class UserCreate(UserBase):
    pass
    
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    skills: List[SkillResponse] = Field(default_factory=list)
    
class UserUpdate(BaseModel):
    username: str | None = Field(None, max_length=100)
    email: EmailStr | None = None      
    bio: str | None = Field(None, max_length=1000)         
    is_active: bool | None = Field(None)
    # created_at: datetime | None 

class ExchangeStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    completed = "completed"
    cancelled = "cancelled"

class ExchangeBase(BaseModel):
    sender_id: int = Field(..., gt=0)
    receiver_id: int = Field(..., gt=0)
    skill_id: int = Field(..., gt=0)
    message: str | None = Field(None, max_length=250)
    hours_proposed: int
    
class ExchangeCreate(ExchangeBase):
    pass

class ExchangeResponse(ExchangeBase):
    id: int
    status: ExchangeStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ExchangeUpdate(BaseModel):
    status: ExchangeStatus

class ReviewBase(BaseModel):
    exchange_id: int = Field(..., gt=0)
    reviewer_id: int = Field(..., gt=0)
    reviewed_id: int = Field(..., gt=0)
    rating: int = Field(..., gt=0, le=10)
    comment: str | None = Field(None, max_length=250)
    
class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ReviewUpdate(BaseModel):
    id: int
    rating: int = Field(..., gt=0, le=10)
    comment: str | None = Field(None, max_length=250)
