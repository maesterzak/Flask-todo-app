from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKeyConstraint
db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable=False)
    todos = relationship('Todo', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.id} {self.name}'

class Todo(db.Model):
    __tablename__ = 'Todo'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('Category.id'), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['category'], ['Category.id'], ondelete='CASCADE'),
    )

   
    def __repr__(self):
        return f'<Todo {self.id} {self.description}'