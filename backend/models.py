from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Table d'association pour les tags de dépenses
expense_tag_table = Table(
    "expense_tags",
    Base.metadata,
    Column("expense_id", Integer, ForeignKey("expenses.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))

    budgets = relationship("Budget", back_populates="user")
    revenues = relationship("Revenue", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    alerts = relationship("Alert", back_populates="user")

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    month = Column(String(7))  # Format YYYY-MM, donc 7 caractères
    amount = Column(Float)

    user = relationship("User", back_populates="budgets")

class Revenue(Base):
    __tablename__ = "revenues"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    source = Column(String(100))
    date = Column(Date)

    user = relationship("User", back_populates="revenues")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    description = Column(String(255))
    category_id = Column(Integer, ForeignKey("categories.id"))
    date = Column(Date)
    type = Column(String(50))

    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
    tags = relationship("Tag", secondary=expense_tag_table, back_populates="expenses")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    expenses = relationship("Expense", back_populates="category")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    expenses = relationship("Expense", secondary=expense_tag_table, back_populates="tags")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String(255))
    trigger_date = Column(Date)

    user = relationship("User", back_populates="alerts")
