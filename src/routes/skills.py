# src/routes/skills.py
# /skills/

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from src.schemas import SkillResponse, SkillCreate, SkillUpdate
from src.database.models import Skill
from src.database.db import get_db

# Цю змінну треба підключити в main.py
router = APIRouter(prefix="/skills", tags=["skills"])

def skill_not_found(skill_id):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"There is no skill by id {skill_id}")
    
def wrong_skill_status():
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail="You can't be teacher and student in a single skill")

@router.get("/health")
def test():
    return {"message": "test works prefix: /skills "}

@router.get("/", response_model=List[SkillResponse])
def get_skills(db: Session=Depends(get_db)):
    skills = db.query(Skill).all()  
    return skills

@router.get("/{skill_id}", response_model=SkillResponse)
def get_skill(skill_id: int, db: Session=Depends(get_db)):
    skill = db.get(Skill, skill_id)
    if not skill:
        skill_not_found(skill_id)
    return skill

@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(skill_id: int, db: Session=Depends(get_db)):
    skill = db.get(Skill, skill_id)
    if not skill:
        skill_not_found(skill_id)
    db.delete(skill)
    db.commit()
    return

@router.post("/", response_model=SkillResponse,
             status_code=status.HTTP_201_CREATED)
def create_skill(skill: SkillCreate, db: Session=Depends(get_db)):
    new_skill = Skill(**skill.model_dump())
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill

@router.put("/{skill_id}", response_model=SkillResponse)
def update_skill(skill_id: int, skill: SkillUpdate, db: Session=Depends(get_db)):
    old_skill = db.get(Skill, skill_id)
    if not old_skill:
        skill_not_found(skill_id)
    
    skill_update = skill.model_dump(exclude_unset=True)
    if "can_teach" in skill_update and "want_learn" in skill_update:
        if skill_update["can_teach"] == skill_update["want_learn"] == True:
            wrong_skill_status()
    elif "can_teach" in skill_update:
        if skill_update["can_teach"] and old_skill.want_learn:
            wrong_skill_status()
    elif "want_learn" in skill_update:
        if skill_update["want_learn"] and old_skill.can_teach:
            wrong_skill_status()
        
    for key, value in skill_update.items():
        setattr(old_skill, key, value)
    db.commit()
    db.refresh(old_skill)
    return old_skill

@router.get("/{skill_id}/matches/", response_model=List[SkillResponse])
def get_skill_matches(skill_id: int, db: Session=Depends(get_db)):
    my_skill = db.get(Skill, skill_id)
    if not my_skill:
        skill_not_found(skill_id)
    same_category = select(Skill).where(Skill.category == my_skill.category, 
                                        Skill.id != skill_id)
    if my_skill.want_learn:
        query = same_category.where(Skill.can_teach == True)
    else:
        query = same_category.where(Skill.want_learn == True)
    matches = db.scalars(query).all()
    return matches
