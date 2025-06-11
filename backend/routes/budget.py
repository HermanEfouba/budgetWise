from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db
from routes.auth import get_current_user
from services.budget_service import BudgetService

router = APIRouter(prefix="/budgets", tags=["budgets"])

@router.post("/", response_model=schemas.Budget)
def create_budget(
    budget: schemas.BudgetCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_budget(db=db, budget=budget, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Budget])
def get_budgets(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.get_budgets_by_user(db, user_id=current_user.id)

@router.get("/month/{month}", response_model=schemas.Budget)
def get_budget_by_month(
    month: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    budget = crud.get_budget_by_month(db, user_id=current_user.id, month=month)
    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@router.get("/dashboard", response_model=schemas.DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return BudgetService.get_dashboard_stats(db, current_user.id)