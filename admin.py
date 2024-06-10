# admin.py

from flask import Blueprint, render_template

# Define the Blueprint with a name and import name
admin_blueprint = Blueprint('admin', __name__)

# Define routes within the Blueprint
@admin_blueprint.route('/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@admin_blueprint.route('/users')
def view_users():
    # Logic to fetch and display users
    return render_template('admin/users.html')
