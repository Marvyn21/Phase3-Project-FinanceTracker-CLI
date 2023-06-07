from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Category", backref="transactions")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    transaction_list = relationship('Transaction', backref="category")


class BudgetGoal(Base):
    __tablename__ = 'budget_goals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    amount = Column(Float, nullable=False)

    category = relationship('Category')