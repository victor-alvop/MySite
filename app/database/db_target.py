from flask_sqlalchemy import SQLAlchemy
from app import db

class Summary(db.Model):
    __tablename__ = 'summary'
    __bind_key__ = 'DB_TARGET_URL'
    __tablename__ = 'summary'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department = db.Column(db.String(100))
    employee_count = db.Column(db.Integer)
    salary_sum = db.Column(db.Float)
    hours_sum = db.Column(db.Integer)
