from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<Category - {self.name}"


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))

    category = relationship("Category", backref="transactions")



class BudgetGoal(Base):
    __tablename__ = 'budget_goal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    amount = Column(Float, nullable=False)

    category = relationship('Category')