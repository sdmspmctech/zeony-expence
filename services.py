from models import db, Revenue, Expense, Client, Project

def update_project_and_client_balances(project_name, client_name):
    if project_name:
        project = Project.query.filter_by(project_name=project_name).first()
        if project:
            total_rev = db.session.query(db.func.sum(Revenue.amount)).filter_by(project_name=project_name, status='Received').scalar() or 0
            total_exp = db.session.query(db.func.sum(Expense.amount)).filter_by(project_name=project_name).scalar() or 0
            project.revenue_received = total_rev
            project.expenses = total_exp
            project.profit = total_rev - total_exp
            
    if client_name:
        client = Client.query.filter_by(client_name=client_name).first()
        if client:
            total_rev = db.session.query(db.func.sum(Revenue.amount)).filter_by(client_name=client_name, status='Received').scalar() or 0
            client.amount_received = total_rev
            client.remaining_amount = client.project_cost - total_rev
            if client.remaining_amount <= 0 and client.project_cost > 0:
                client.payment_status = 'Completed'
            elif client.amount_received > 0:
                client.payment_status = 'Partial'
            else:
                client.payment_status = 'Pending'
                
    db.session.commit()
