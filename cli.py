import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Transaction, Category

engine = create_engine('sqlite:///finance_tracker.db')
Session = sessionmaker(bind=engine)

def list_categories():
    session = Session()
    categories_objects = session.query(Category).all()
    category_ids = []
    for category in categories_objects:
        category_ids.append({category.id: category.name})
    return category_ids

@click.group()
def cli():
    """Finance Tracker CLI"""
    click.echo("Welcome to Finance Tracker CLI!")

@cli.command()
@click.option('--amount', type=float, prompt='Enter the transaction amount')
@click.option('--category-id', type=str, prompt=f'Enter the transaction category id. Options : {list_categories()}')
@click.option('--description', type=str, prompt='Enter the transaction description')
def add_transaction(amount, category_id, description):
    session = Session()
    transaction = Transaction(amount=amount, description=description)
    category_obj = session.query(Category).filter_by(id=category_id).first()
    if not category_obj:
        category_obj = Category(id=category_id)
        session.add(category_obj)
    transaction.category = category_obj
    session.add(transaction)
    session.commit()
    click.echo(f"Added transaction: Amount={amount}, Category ID={category_id}, Description={description}")

@cli.command()
@click.option('--transaction-id', type=int, prompt='Enter the transaction ID')
@click.option('--category', type=str, prompt='Enter the transaction category')
def categorize(transaction_id, category):
    session = Session()
    transaction = session.query(Transaction).filter_by(id=transaction_id).first()
    if not transaction:
        click.echo(f"Transaction {transaction_id} not found.")
        return
    category_obj = session.query(Category).filter_by(name=category).first()
    if not category_obj:
        category_obj = Category(name=category)
        session.add(category_obj)
    transaction.category = category_obj
    session.commit()
    click.echo(f"Transaction {transaction_id} categorized as {category}")

@cli.command()
@click.option('--category', type=str, prompt='Enter the category name')
def generate_report(category):
    session = Session()
    transactions = session.query(Transaction).join(Category).filter(Category.name == category).all()
    if not transactions:
        click.echo(f"No transactions found for category: {category}")
        return
    click.echo(f"Report for category: {category}")
    for transaction in transactions:
        click.echo(f"Transaction ID: {transaction.id}, Amount: {transaction.amount}, Description: {transaction.description}")

if __name__ == '__main__':
    cli()