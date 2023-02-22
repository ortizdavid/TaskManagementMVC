from config import *
from models.role import Role
from models.user import User
from flask import render_template, request, redirect, url_for, session

class RoleController:

	@app.route('/roles', methods=['GET'])
	def show_roles():
		roles = Role.get_all()
		num_rows = len(roles)
		return render_template('role/show.html', roles=roles, num_rows=num_rows, logged_user=User.get_logged_user())


	@app.route('/roles/<id>/details', methods=['GET'])
	def role_details(id):
		role = Role.get_data_by_id(id)
		if role:
			return render_template('role/details.html', role=role, logged_user=User.get_logged_user())
		else:
			return render_template('error/404.html')


	@app.route('/roles/add', methods=['GET', 'POST'])
	def add_role():
		if request.method == 'GET': 
			return render_template('role/add.html', logged_user=User.get_logged_user())
		else:
			role_name = request.form['role_name']
			role = Role(role_name)
			role.save()
			return redirect(url_for('show_roles'))