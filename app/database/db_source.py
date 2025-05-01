from flask_sqlalchemy import SQLAlchemy
from app import db


class Employee(db.Model):
    __bind_key__ = 'DB_SOURCE_URL'
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    department = db.Column(db.String(100))
    salary = db.Column(db.Numeric(10, 2))
    hours = db.Column(db.Integer)