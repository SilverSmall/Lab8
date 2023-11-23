from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Підключення до бази даних
engine = create_engine('sqlite:///personal_expenses.db', echo=True)
Base = declarative_base()

# Оголошення класів моделей
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    expenses = relationship('Expense', back_populates='category')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    expenses = relationship('Expense', back_populates='user')

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    category = relationship('Category', back_populates='expenses')
    user = relationship('User', back_populates='expenses')

# Створення таблиць
Base.metadata.create_all(engine)
# Підключення до бази даних
Session = sessionmaker(bind=engine)
session = Session()

# CRUD операції

# Create (створення)
def create_category(name):
    new_category = Category(name=name)
    session.add(new_category)
    session.commit()

def create_user(username):
    new_user = User(username=username)
    session.add(new_user)
    session.commit()

def create_expense(amount, description, category_id, user_id):
    new_expense = Expense(amount=amount, description=description, category_id=category_id, user_id=user_id)
    session.add(new_expense)
    session.commit()

# Read (читання)
def get_all_categories():
    return session.query(Category).all()

def get_all_users():
    return session.query(User).all()

def get_expenses_by_user(user_id):
    return session.query(Expense).filter_by(user_id=user_id).all()

# Update (оновлення)
def update_category_name(category_id, new_name):
    category = session.query(Category).get(category_id)
    if category:
        category.name = new_name
        session.commit()

# Delete (видалення)
def delete_user(user_id):
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()

# Використання функцій:
create_category('Food')
create_category('Transport')
create_user('John')
create_user('Jane')
create_expense(20.5, 'Lunch', 1, 1)  # 20.5 expense for Food category by John

categories = get_all_categories()
for category in categories:
    print(category.id, category.name)

john_expenses = get_expenses_by_user(1)
for expense in john_expenses:
    print(expense.amount, expense.description)

update_category_name(1, 'Groceries')
delete_user(2)  # Delete Jane

# Закриття сесії
session.close()
