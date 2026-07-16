from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Revenue, Client, Project
from services import update_project_and_client_balances
from datetime import datetime

bp = Blueprint('revenue', __name__)

@bp.route('/')
@login_required
def index():
    revenues = Revenue.query.order_by(Revenue.date.desc()).all()
    clients = Client.query.all()
    projects = Project.query.all()
    return render_template('revenue/index.html', revenues=revenues, clients=clients, projects=projects)

@bp.route('/add', methods=['POST'])
@login_required
def add():
    date_str = request.form.get('date')
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.utcnow().date()
    
    new_revenue = Revenue(
        date=date_obj,
        client_name=request.form.get('client_name'),
        project_name=request.form.get('project_name'),
        description=request.form.get('description'),
        amount=float(request.form.get('amount', 0)),
        payment_mode=request.form.get('payment_mode'),
        status=request.form.get('status'),
        remarks=request.form.get('remarks')
    )
    db.session.add(new_revenue)
    db.session.commit()
    
    update_project_and_client_balances(new_revenue.project_name, new_revenue.client_name)
    flash('Revenue added successfully.', 'success')
    return redirect(url_for('revenue.index'))
