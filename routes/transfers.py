from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Transfer
from datetime import datetime

bp = Blueprint('transfers', __name__)

@bp.route('/')
@login_required
def index():
    transfers = Transfer.query.order_by(Transfer.date.desc(), Transfer.id.desc()).all()
    return render_template('transfers/index.html', transfers=transfers)

@bp.route('/add', methods=['POST'])
@login_required
def add():
    date_str = request.form.get('date')
    amount = request.form.get('amount')
    transfer_type = request.form.get('transfer_type')
    remarks = request.form.get('remarks')
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        amount_float = float(amount)
        
        new_transfer = Transfer(
            date=date_obj,
            transfer_type=transfer_type,
            amount=amount_float,
            remarks=remarks
        )
        db.session.add(new_transfer)
        db.session.commit()
        flash('Transfer recorded successfully.', 'success')
    except Exception as e:
        flash(f'Error recording transfer: {str(e)}', 'error')
        
    return redirect(url_for('transfers.index'))
