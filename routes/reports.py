from flask import Blueprint, render_template, request
from flask_login import login_required
from models import db, Revenue, Expense, Client, Project
from datetime import datetime, date

bp = Blueprint('reports', __name__)

@bp.route('/')
@login_required
def index():
    today = date.today()
    
    todays_revenue = db.session.query(db.func.sum(Revenue.amount)).filter(db.func.date(Revenue.date) == today).scalar() or 0
    todays_expenses = db.session.query(db.func.sum(Expense.amount)).filter(db.func.date(Expense.date) == today).scalar() or 0
    
    revenues = Revenue.query.order_by(Revenue.date.desc()).all()
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    projects = Project.query.all()
    
    return render_template('reports/index.html', 
                           todays_revenue=todays_revenue,
                           todays_expenses=todays_expenses,
                           revenues=revenues,
                           expenses=expenses,
                           projects=projects)
