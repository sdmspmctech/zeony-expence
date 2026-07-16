from flask import Blueprint, render_template
from flask_login import login_required
from models import db, Revenue, Expense, Client, Project, Setting
from sqlalchemy import func

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
@login_required
def index():
    setting = Setting.query.first()
    opening_cash = setting.opening_cash if setting else 0.0
    opening_online = setting.opening_online if setting else 0.0

    total_revenue_cash = db.session.query(func.sum(Revenue.amount)).filter_by(payment_mode='Cash', status='Received').scalar() or 0.0
    total_revenue_online = db.session.query(func.sum(Revenue.amount)).filter_by(payment_mode='Online', status='Received').scalar() or 0.0
    
    total_expense_cash = db.session.query(func.sum(Expense.amount)).filter_by(payment_mode='Cash').scalar() or 0.0
    total_expense_online = db.session.query(func.sum(Expense.amount)).filter_by(payment_mode='Online').scalar() or 0.0
    
    # Calculate Transfers
    from models import Transfer
    total_cash_to_online = db.session.query(func.sum(Transfer.amount)).filter_by(transfer_type='Cash to Online').scalar() or 0.0
    total_online_to_cash = db.session.query(func.sum(Transfer.amount)).filter_by(transfer_type='Online to Cash').scalar() or 0.0
    
    cash_available = opening_cash + total_revenue_cash - total_expense_cash - total_cash_to_online + total_online_to_cash
    online_balance = opening_online + total_revenue_online - total_expense_online + total_cash_to_online - total_online_to_cash
    
    total_revenue = total_revenue_cash + total_revenue_online
    total_expenses = total_expense_cash + total_expense_online
    total_company_balance = cash_available + online_balance
    
    total_clients = Client.query.count()
    total_projects = Project.query.count()
    
    # Basic data for charts
    income_data = [total_revenue_cash, total_revenue_online]
    expense_data = [total_expense_cash, total_expense_online]
    balance_data = [cash_available, online_balance]

    return render_template('dashboard.html', 
                           total_revenue=total_revenue,
                           total_expenses=total_expenses,
                           cash_available=cash_available,
                           online_balance=online_balance,
                           total_company_balance=total_company_balance,
                           total_clients=total_clients,
                           total_projects=total_projects,
                           income_data=income_data,
                           expense_data=expense_data,
                           balance_data=balance_data)
