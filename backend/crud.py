from sqlalchemy.orm import Session
from sqlalchemy import and_, extract
from typing import List, Optional
from datetime import date
import models
import schemas
from services.auth import get_password_hash

# --- User ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        name=user.name,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Budget ---
def get_budget(db: Session, budget_id: int):
    return db.query(models.Budget).filter(models.Budget.id == budget_id).first()

def get_budgets_by_user(db: Session, user_id: int):
    return db.query(models.Budget).filter(models.Budget.user_id == user_id).all()

def get_budget_by_month(db: Session, user_id: int, month: str):
    return db.query(models.Budget).filter(
        and_(models.Budget.user_id == user_id, models.Budget.month == month)
    ).first()

def create_budget(db: Session, budget: schemas.BudgetCreate, user_id: int):
    # Check if budget already exists for this month
    existing_budget = get_budget_by_month(db, user_id, budget.month)
    if existing_budget:
        existing_budget.amount = budget.amount
        db.commit()
        db.refresh(existing_budget)
        return existing_budget
    
    db_budget = models.Budget(
        user_id=user_id,
        month=budget.month,
        amount=budget.amount
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

# --- Revenue ---
def get_revenue(db: Session, revenue_id: int):
    return db.query(models.Revenue).filter(models.Revenue.id == revenue_id).first()

def get_revenues_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Revenue).filter(
        models.Revenue.user_id == user_id
    ).offset(skip).limit(limit).all()

def get_revenues_by_date_range(db: Session, user_id: int, start_date: date, end_date: date):
    return db.query(models.Revenue).filter(
        and_(
            models.Revenue.user_id == user_id,
            models.Revenue.date >= start_date,
            models.Revenue.date <= end_date
        )
    ).all()

def create_revenue(db: Session, revenue: schemas.RevenueCreate, user_id: int):
    db_revenue = models.Revenue(
        user_id=user_id,
        amount=revenue.amount,
        source=revenue.source,
        date=revenue.date
    )
    db.add(db_revenue)
    db.commit()
    db.refresh(db_revenue)
    return db_revenue

def update_revenue(db: Session, revenue_id: int, revenue: schemas.RevenueCreate):
    db_revenue = get_revenue(db, revenue_id)
    if db_revenue:
        db_revenue.amount = revenue.amount
        db_revenue.source = revenue.source
        db_revenue.date = revenue.date
        db.commit()
        db.refresh(db_revenue)
    return db_revenue

def delete_revenue(db: Session, revenue_id: int):
    db_revenue = get_revenue(db, revenue_id)
    if db_revenue:
        db.delete(db_revenue)
        db.commit()
    return db_revenue

# --- Expense ---
def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()

def get_expenses_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Expense).filter(
        models.Expense.user_id == user_id
    ).offset(skip).limit(limit).all()

def get_expenses_by_date_range(db: Session, user_id: int, start_date: date, end_date: date):
    return db.query(models.Expense).filter(
        and_(
            models.Expense.user_id == user_id,
            models.Expense.date >= start_date,
            models.Expense.date <= end_date
        )
    ).all()

def get_expenses_by_category(db: Session, user_id: int, category_id: int):
    return db.query(models.Expense).filter(
        and_(
            models.Expense.user_id == user_id,
            models.Expense.category_id == category_id
        )
    ).all()

def create_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int):
    db_expense = models.Expense(
        user_id=user_id,
        amount=expense.amount,
        description=expense.description,
        category_id=expense.category_id,
        date=expense.date,
        type=expense.type
    )
    
    # Add tags if provided
    if expense.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(expense.tag_ids)).all()
        db_expense.tags = tags
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def update_expense(db: Session, expense_id: int, expense: schemas.ExpenseCreate):
    db_expense = get_expense(db, expense_id)
    if db_expense:
        db_expense.amount = expense.amount
        db_expense.description = expense.description
        db_expense.category_id = expense.category_id
        db_expense.date = expense.date
        db_expense.type = expense.type
        
        # Update tags
        if expense.tag_ids:
            tags = db.query(models.Tag).filter(models.Tag.id.in_(expense.tag_ids)).all()
            db_expense.tags = tags
        else:
            db_expense.tags = []
            
        db.commit()
        db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int):
    db_expense = get_expense(db, expense_id)
    if db_expense:
        db.delete(db_expense)
        db.commit()
    return db_expense

# --- Category ---
def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# --- Tag ---
def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()

def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tag).offset(skip).limit(limit).all()

def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

# --- Alert ---
def get_alert(db: Session, alert_id: int):
    return db.query(models.Alert).filter(models.Alert.id == alert_id).first()

def get_alerts_by_user(db: Session, user_id: int):
    return db.query(models.Alert).filter(models.Alert.user_id == user_id).all()

def create_alert(db: Session, alert: schemas.AlertCreate, user_id: int):
    db_alert = models.Alert(
        user_id=user_id,
        message=alert.message,
        trigger_date=alert.trigger_date
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert