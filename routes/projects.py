from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Project, Client
from services import update_project_and_client_balances

bp = Blueprint('projects', __name__)

@bp.route('/')
@login_required
def index():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    clients = Client.query.all()
    return render_template('projects/index.html', projects=projects, clients=clients)

@bp.route('/add', methods=['POST'])
@login_required
def add():
    new_project = Project(
        project_name=request.form.get('project_name'),
        client_name=request.form.get('client_name'),
        total_value=float(request.form.get('total_value', 0))
    )
    db.session.add(new_project)
    db.session.commit()
    
    update_project_and_client_balances(new_project.project_name, None)
    flash('Project added successfully.', 'success')
    return redirect(url_for('projects.index'))
