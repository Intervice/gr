from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from src.schemas import ExchangeResponse, ExchangeCreate, ExchangeUpdate
from src.database.models import Exchange
from src.database.db import get_db

router = APIRouter(prefix="/exchanges", tags=["exchanges"])

def exchange_not_found(exchange_id):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"There is no exchange by id {exchange_id}")
    
@router.get("/health")
def test():
    return {"message": "test words | prefix: /exchanges"}

# @router.get("/", response_model=List[ExchangeResponse])
# def get_exchanges(db: Session=Depends(get_db)):
#     exchanges = db.query(exchange).all()  
#     return exchanges

# @router.get("/{exchange_id}", response_model=ExchangeResponse)
# def get_exchanges(exchange_id: int, db: Session=Depends(get_db)):
#     exchange = db.get(exchange, exchange_id)
#     if not exchange:
#         exchange_not_found(exchange_id)
#     return exchange

# @router.post("/{exchange_id}", response_model=ExchangeResponse)
# def create_exchange(exchange: ExchangeCreate, db: Session=Depends(get_db)):
#     try:
#         new_exchange = exchange(**exchange.model_dump())
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail=f"Error: {e}")
#     db.add(new_exchange)
#     db.commit()
#     db.refresh(new_exchange)
#     return new_exchange

# @router.delete("/{exchange_id}", response_model=ExchangeResponse)
# def delete_exchange(exchange_id: int, db: Session=Depends(get_db)):
#     exchange = db.get(exchange, exchange_id)
#     if not exchange:
#         exchange_not_found(exchange_id)
#     db.delete(exchange)
#     db.commit()
#     return exchange
    
# @router.put("/{exchange_id}", response_model=ExchangeResponse)
# def edit_exchange(exchange_id: int, exchange_new: ExchangeUpdate, db: Session=Depends(get_db)):
#     exchange = db.get(exchange, exchange_id)
#     if not exchange:
#         exchange_not_found(exchange_id)
#     update_exchange = exchange_new.model_dump(exclude_unset=True)
#     for attr, new_value in update_exchange.items():
#         setattr(exchange, attr, new_value)
#     db.commit()
#     db.refresh(exchange)
#     return exchange

