from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from src.schemas import ReviewResponse, ReviewCreate, ReviewUpdate
from src.database.models import Review
from src.database.db import get_db

router = APIRouter(prefix="/reviews", tags=["reviews"])

def review_not_found(review_id):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"There is no review by id {review_id}")
    
@router.get("/health")
def test():
    return {"message": "test words | prefix: /reviews"}

@router.get("/", response_model=List[ReviewResponse])
def get_reviews(db: Session=Depends(get_db)):
    reviews = db.query(Review).all()  
    return reviews

@router.get("/{review_id}", response_model=ReviewResponse)
def get_reviews(review_id: int, db: Session=Depends(get_db)):
    review = db.get(review, review_id)
    if not review:
        review_not_found(review_id)
    return review

@router.post("/{review_id}", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session=Depends(get_db)):
    try:
        new_review = review(**review.model_dump())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Error: {e}")
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.delete("/{review_id}", response_model=ReviewResponse)
def delete_review(review_id: int, db: Session=Depends(get_db)):
    review = db.get(review, review_id)
    if not review:
        review_not_found(review_id)
    db.delete(review)
    db.commit()
    return review
    
@router.put("/{review_id}", response_model=ReviewResponse)
def edit_review(review_id: int, review_new: ReviewUpdate, db: Session=Depends(get_db)):
    review = db.get(review, review_id)
    if not review:
        review_not_found(review_id)
    update_review = review_new.model_dump(exclude_unset=True)
    for attr, new_value in update_review.items():
        setattr(review, attr, new_value)
    db.commit()
    db.refresh(review)
    return review

