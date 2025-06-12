from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import crud
import schemas
from database import get_db

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=schemas.Expense)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db)
):
    # Get user_id from request body
    user_id = getattr(expense, 'user_id', None)
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    return crud.create_expense(db=db, expense=expense, user_id=user_id)

@router.get("/", response_model=List[schemas.Expense])
def get_expenses(
    user_id: int = Query(...),
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if start_date and end_date:
        return crud.get_expenses_by_date_range(db, user_id, start_date, end_date)
    elif category_id:
        return crud.get_expenses_by_category(db, user_id, category_id)
    else:
        return crud.get_expenses_by_user(db, user_id, skip, limit)

@router.get("/{expense_id}", response_model=schemas.Expense)
def get_expense(
    expense_id: int,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    expense = crud.get_expense(db, expense_id=expense_id)
    if expense is None or expense.user_id != user_id:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.put("/{expense_id}", response_model=schemas.Expense)
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseCreate,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None or db_expense.user_id != user_id:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return crud.update_expense(db=db, expense_id=expense_id, expense=expense)

@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None or db_expense.user_id != user_id:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    crud.delete_expense(db=db, expense_id=expense_id)
    return {"message": "Expense deleted successfully"}