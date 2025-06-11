from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, date
from typing import List, Optional
import models
import schemas

class BudgetService:
    @staticmethod
    def calculate_current_balance(db: Session, user_id: int) -> float:
        """Calculate current balance for a user"""
        total_revenue = db.query(func.sum(models.Revenue.amount)).filter(
            models.Revenue.user_id == user_id
        ).scalar() or 0
        
        total_expenses = db.query(func.sum(models.Expense.amount)).filter(
            models.Expense.user_id == user_id
        ).scalar() or 0
        
        return float(total_revenue - total_expenses)
    
    @staticmethod
    def get_monthly_stats(db: Session, user_id: int, year: int, month: int) -> schemas.MonthlyStats:
        """Get monthly statistics for a user"""
        revenue_sum = db.query(func.sum(models.Revenue.amount)).filter(
            models.Revenue.user_id == user_id,
            extract('year', models.Revenue.date) == year,
            extract('month', models.Revenue.date) == month
        ).scalar() or 0
        
        expense_sum = db.query(func.sum(models.Expense.amount)).filter(
            models.Expense.user_id == user_id,
            extract('year', models.Expense.date) == year,
            extract('month', models.Expense.date) == month
        ).scalar() or 0
        
        return schemas.MonthlyStats(
            month=f"{year}-{month:02d}",
            total_revenue=float(revenue_sum),
            total_expenses=float(expense_sum),
            balance=float(revenue_sum - expense_sum)
        )
    
    @staticmethod
    def get_category_stats(db: Session, user_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[schemas.CategoryStats]:
        """Get expense statistics by category"""
        query = db.query(
            models.Category.name,
            func.sum(models.Expense.amount).label('total')
        ).join(
            models.Expense
        ).filter(
            models.Expense.user_id == user_id
        )
        
        if start_date:
            query = query.filter(models.Expense.date >= start_date)
        if end_date:
            query = query.filter(models.Expense.date <= end_date)
            
        results = query.group_by(models.Category.name).all()
        
        total_expenses = sum(result.total for result in results)
        
        return [
            schemas.CategoryStats(
                category_name=result.name,
                total_amount=float(result.total),
                percentage=float((result.total / total_expenses) * 100) if total_expenses > 0 else 0
            )
            for result in results
        ]
    
    @staticmethod
    def get_dashboard_stats(db: Session, user_id: int) -> schemas.DashboardStats:
        """Get comprehensive dashboard statistics"""
        current_date = datetime.now()
        current_month = f"{current_date.year}-{current_date.month:02d}"
        
        # Get current month budget
        budget = db.query(models.Budget).filter(
            models.Budget.user_id == user_id,
            models.Budget.month == current_month
        ).first()
        
        monthly_budget = float(budget.amount) if budget else 0.0
        
        # Get monthly stats
        monthly_stats = BudgetService.get_monthly_stats(
            db, user_id, current_date.year, current_date.month
        )
        
        # Get category stats for current month
        start_of_month = date(current_date.year, current_date.month, 1)
        category_stats = BudgetService.get_category_stats(
            db, user_id, start_of_month, current_date.date()
        )
        
        current_balance = BudgetService.calculate_current_balance(db, user_id)
        budget_remaining = monthly_budget - monthly_stats.total_expenses
        
        return schemas.DashboardStats(
            current_balance=current_balance,
            monthly_budget=monthly_budget,
            budget_remaining=budget_remaining,
            total_expenses_this_month=monthly_stats.total_expenses,
            total_revenue_this_month=monthly_stats.total_revenue,
            top_categories=category_stats[:5]  # Top 5 categories
        )