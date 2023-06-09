from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Transaction, Category, BudgetGoal

engine = create_engine('sqlite:///finance_tracker.db')

Session = sessionmaker(bind=engine)
session = Session()


transaction1 = Transaction(amount=100, description="Transaction 1")
transaction2 = Transaction(amount=200, description="Transaction 2")

category_name = "Category 1"
category = session.query(Category).filter_by(name=category_name).first()

if not category:
    category = Category(name=category_name)

transaction1.category_list.append(category)
transaction2.category_list.append(category)

session.add_all([transaction1, transaction2])
session.commit()

session.close()

# category_name = "test category"
# amount = 10
# description = "test description"
# category_id = 1

# transaction = Transaction(
#     amount=amount,
#     description=description,
#     category_id = category_id
# )
# session.add(transaction)
# session.commit()

# breakpoint()