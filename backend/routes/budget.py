from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db
from services.budget_service import BudgetService

router = APIRouter(prefix="/budgets", tags=["budgets"])

@router.post("/", response_model=schemas.Budget)
def create_budget(
    budget: schemas.BudgetCreate,
    db: Session = Depends(get_db)
):
    # Get user_id from request body
    user_id = getattr(budget, 'user_id', None)
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    return crud.create_budget(db=db, budget=budget, user_id=user_id)

@router.get("/", response_model=List[schemas.Budget])
def get_budgets(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    return crud.get_budgets_by_user(db, user_id=user_id)

@router.get("/month/{month}", response_model=schemas.Budget)
def get_budget_by_month(
    month: str,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    budget = crud.get_budget_by_month(db, user_id=user_id, month=month)
    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@router.get("/dashboard", response_model=schemas.DashboardStats)
def get_dashboard_stats(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    return BudgetService.get_dashboard_stats(db, user_id)