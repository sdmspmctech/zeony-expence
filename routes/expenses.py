from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Expense, Project
from services import update_project_and_client_balances
from datetime import datetime

bp = Blueprint('expenses', __name__)

CATEGORIES = [
    'Office Rent', 'Internet', 'Electricity', 'Travel', 'Fuel', 'Food',
    'Software', 'Hosting', 'Domain', 'Marketing', 'Salary', 
    'Freelancer Payment', 'Office Purchase', 'Miscellaneous'
]

@bp.route('/')
@login_required
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    projects = Project.query.all()
    return render_template('expenses/index.html', expenses=expenses, projects=projects, categories=CATEGORIES)

@bp.route('/add', methods=['POST'])
@login_required
def add():
    date_str = request.form.get('date')
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.utcnow().date()
    
    new_expense = Expense(
        date=date_obj,
        title=request.form.get('title'),
        category=request.form.get('category'),
        project_name=request.form.get('project_name'),
        amount=float(request.form.get('amount', 0)),
        payment_mode=request.form.get('payment_mode'),
        remarks=request.form.get('remarks')
    )
    db.session.add(new_expense)
    db.session.commit()
    
    if new_expense.project_name:
        update_project_and_client_balances(new_expense.project_name, None)
        
    flash('Expense added successfully.', 'success')
    return redirect(url_for('expenses.index'))
