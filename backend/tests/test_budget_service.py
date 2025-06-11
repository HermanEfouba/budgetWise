import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from services.budget_service import BudgetService
import models
from datetime import date, datetime

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_budget.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture
def test_user(db_session):
    user = models.User(
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_category(db_session):
    category = models.Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category

def test_calculate_current_balance_empty(db_session, test_user):
    balance = BudgetService.calculate_current_balance(db_session, test_user.id)
    assert balance == 0.0

def test_calculate_current_balance_with_data(db_session, test_user, test_category):
    # Add revenue
    revenue = models.Revenue(
        user_id=test_user.id,
        amount=1000.0,
        source="Salary",
        date=date.today()
    )
    db_session.add(revenue)
    
    # Add expense
    expense = models.Expense(
        user_id=test_user.id,
        amount=300.0,
        description="Groceries",
        category_id=test_category.id,
        date=date.today(),
        type="variable"
    )
    db_session.add(expense)
    db_session.commit()
    
    balance = BudgetService.calculate_current_balance(db_session, test_user.id)
    assert balance == 700.0

def test_get_monthly_stats(db_session, test_user, test_category):
    current_date = datetime.now()
    
    # Add revenue for current month
    revenue = models.Revenue(
        user_id=test_user.id,
        amount=2000.0,
        source="Salary",
        date=date(current_date.year, current_date.month, 15)
    )
    db_session.add(revenue)
    
    # Add expense for current month
    expense = models.Expense(
        user_id=test_user.id,
        amount=500.0,
        description="Rent",
        category_id=test_category.id,
        date=date(current_date.year, current_date.month, 1),
        type="fixe"
    )
    db_session.add(expense)
    db_session.commit()
    
    stats = BudgetService.get_monthly_stats(
        db_session, test_user.id, current_date.year, current_date.month
    )
    
    assert stats.total_revenue == 2000.0
    assert stats.total_expenses == 500.0
    assert stats.balance == 1500.0
    assert stats.month == f"{current_date.year}-{current_date.month:02d}"

def test_get_category_stats(db_session, test_user, test_category):
    # Add multiple expenses in the same category
    expense1 = models.Expense(
        user_id=test_user.id,
        amount=100.0,
        description="Expense 1",
        category_id=test_category.id,
        date=date.today(),
        type="variable"
    )
    expense2 = models.Expense(
        user_id=test_user.id,
        amount=200.0,
        description="Expense 2",
        category_id=test_category.id,
        date=date.today(),
        type="variable"
    )
    db_session.add_all([expense1, expense2])
    db_session.commit()
    
    stats = BudgetService.get_category_stats(db_session, test_user.id)
    
    assert len(stats) == 1
    assert stats[0].category_name == "Test Category"
    assert stats[0].total_amount == 300.0
    assert stats[0].percentage == 100.0