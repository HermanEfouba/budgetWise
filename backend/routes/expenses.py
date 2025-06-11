from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import crud
import schemas
from database import get_db
from routes.auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=schemas.Expense)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_expense(db=db, expense=expense, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Expense])
def get_expenses(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    if start_date and end_date:
        return crud.get_expenses_by_date_range(db, current_user.id, start_date, end_date)
    elif category_id:
        return crud.get_expenses_by_category(db, current_user.id, category_id)
    else:
        return crud.get_expenses_by_user(db, current_user.id, skip, limit)

@router.get("/{expense_id}", response_model=schemas.Expense)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    expense = crud.get_expense(db, expense_id=expense_id)
    if expense is None or expense.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.put("/{expense_id}", response_model=schemas.Expense)
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None or db_expense.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return crud.update_expense(db=db, expense_id=expense_id, expense=expense)

@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None or db_expense.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    crud.delete_expense(db=db, expense_id=expense_id)
    return {"message": "Expense deleted successfully"}