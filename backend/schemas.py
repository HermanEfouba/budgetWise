from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

# Base schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr

class BudgetBase(BaseModel):
    month: str
    amount: float

class RevenueBase(BaseModel):
    amount: float
    source: str
    date: date

class ExpenseBase(BaseModel):
    amount: float
    description: str
    date: date
    type: str
    category_id: int

class CategoryBase(BaseModel):
    name: str

class TagBase(BaseModel):
    name: str

class AlertBase(BaseModel):
    message: str
    trigger_date: date

# Create schemas
class UserCreate(UserBase):
    password: str

class BudgetCreate(BudgetBase):
    pass

class RevenueCreate(RevenueBase):
    pass

class ExpenseCreate(ExpenseBase):
    tag_ids: Optional[List[int]] = []

class CategoryCreate(CategoryBase):
    pass

class TagCreate(TagBase):
    pass

class AlertCreate(AlertBase):
    pass

# Response schemas
class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class Budget(BudgetBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

class Revenue(RevenueBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

class Category(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class Tag(TagBase):
    id: int
    
    class Config:
        from_attributes = True

class Expense(ExpenseBase):
    id: int
    user_id: int
    category: Optional[Category] = None
    tags: List[Tag] = []
    
    class Config:
        from_attributes = True

class Alert(AlertBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

# Statistics schemas
class MonthlyStats(BaseModel):
    month: str
    total_revenue: float
    total_expenses: float
    balance: float

class CategoryStats(BaseModel):
    category_name: str
    total_amount: float
    percentage: float

class DashboardStats(BaseModel):
    current_balance: float
    monthly_budget: float
    budget_remaining: float
    total_expenses_this_month: float
    total_revenue_this_month: float
    top_categories: List[CategoryStats]