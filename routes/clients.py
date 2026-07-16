from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Client
from services import update_project_and_client_balances

bp = Blueprint('clients', __name__)

@bp.route('/')
@login_required
def index():
    clients = Client.query.order_by(Client.created_at.desc()).all()
    return render_template('clients/index.html', clients=clients)

@bp.route('/add', methods=['POST'])
@login_required
def add():
    new_client = Client(
        client_name=request.form.get('client_name'),
        company_name=request.form.get('company_name'),
        phone=request.form.get('phone'),
        email=request.form.get('email'),
        project_name=request.form.get('project_name'),
        project_cost=float(request.form.get('project_cost', 0))
    )
    db.session.add(new_client)
    db.session.commit()
    
    update_project_and_client_balances(None, new_client.client_name)
    flash('Client added successfully.', 'success')
    return redirect(url_for('clients.index'))
