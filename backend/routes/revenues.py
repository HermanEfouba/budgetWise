from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import crud
import schemas
from database import get_db

router = APIRouter(prefix="/revenues", tags=["revenues"])

@router.post("/", response_model=schemas.Revenue)
def create_revenue(
    revenue: schemas.RevenueCreate,
    db: Session = Depends(get_db)
):
    # Get user_id from request body
    user_id = getattr(revenue, 'user_id', None)
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    return crud.create_revenue(db=db, revenue=revenue, user_id=user_id)

@router.get("/", response_model=List[schemas.Revenue])
def get_revenues(
    user_id: int = Query(...),
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    if start_date and end_date:
        return crud.get_revenues_by_date_range(db, user_id, start_date, end_date)
    else:
        return crud.get_revenues_by_user(db, user_id, skip, limit)

@router.get("/{revenue_id}", response_model=schemas.Revenue)
def get_revenue(
    revenue_id: int,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    revenue = crud.get_revenue(db, revenue_id=revenue_id)
    if revenue is None or revenue.user_id != user_id:
        raise HTTPException(status_code=404, detail="Revenue not found")
    return revenue

@router.put("/{revenue_id}", response_model=schemas.Revenue)
def update_revenue(
    revenue_id: int,
    revenue: schemas.RevenueCreate,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    db_revenue = crud.get_revenue(db, revenue_id=revenue_id)
    if db_revenue is None or db_revenue.user_id != user_id:
        raise HTTPException(status_code=404, detail="Revenue not found")
    
    return crud.update_revenue(db=db, revenue_id=revenue_id, revenue=revenue)

@router.delete("/{revenue_id}")
def delete_revenue(
    revenue_id: int,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    db_revenue = crud.get_revenue(db, revenue_id=revenue_id)
    if db_revenue is None or db_revenue.user_id != user_id:
        raise HTTPException(status_code=404, detail="Revenue not found")
    
    crud.delete_revenue(db=db, revenue_id=revenue_id)
    return {"message": "Revenue deleted successfully"}