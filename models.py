from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Revenue(db.Model):
    __tablename__ = 'revenue'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    client_name = db.Column(db.String(100), nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    amount = db.Column(db.Float, nullable=False)
    payment_mode = db.Column(db.String(50), nullable=False) # Cash, Online
    status = db.Column(db.String(50), nullable=False) # Received, Pending
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    project_name = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    payment_mode = db.Column(db.String(50), nullable=False) # Cash, Online
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(150))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    project_name = db.Column(db.String(100))
    project_cost = db.Column(db.Float, default=0.0)
    amount_received = db.Column(db.Float, default=0.0)
    remaining_amount = db.Column(db.Float, default=0.0)
    payment_status = db.Column(db.String(50), default='Pending') # Pending, Partial, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    total_value = db.Column(db.Float, default=0.0)
    revenue_received = db.Column(db.Float, default=0.0)
    expenses = db.Column(db.Float, default=0.0)
    profit = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    opening_cash = db.Column(db.Float, default=0.0)
    opening_online = db.Column(db.Float, default=0.0)
