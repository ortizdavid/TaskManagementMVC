from config import *
from helpers.file_uploader import *
from helpers.password_handler import *
from models.user import User
from models.role import Role
from flask import render_template, request, redirect, url_for, session

class UserController:

	@app.route('/users', methods=['GET'])
	def show_users():
		users = User.get_all_data()
		num_rows = len(users)
		return render_template('user/show.html', users=users, num_rows=num_rows, logged_user=User.get_logged_user())


	@app.route('/users/<id>/details', methods=['GET'])
	def user_details(id):
		user = User.get_data_by_id(id)
		if user:
			return render_template('user/details.html', user=user, logged_user=User.get_logged_user())
		else:
			return render_template('errorr/404.html')


	@app.route('/user-data', methods=['GET'])
	def get_user_data():
		logged_user = User.get_logged_user()
		data = User.get_data_by_id(logged_user.user_id)
		return render_template('user/user-data.html', data=data, logged_user=logged_user)


	@app.route('/users/add', methods=['GET', 'POST'])
	def add_user():
		roles = Role.get_all()
		logged_user=User.get_logged_user()

		if request.method == 'GET': 
			return render_template('user/add.html', logged_user=logged_user, roles=roles)
		else:
			user_name = request.form['user_name']
			role_id = request.form['role_id']
			password = request.form['password']
			encrypt_password = PasswordHandler.generate(password)
			image = ''
			user = User(role_id, user_name, encrypt_password, image)
			user.save()
			return redirect(url_for('show_users'))


	@app.route('/users/<id>/edit', methods=['GET', 'POST'])
	def edit_user(id):
		user = User.get_by_id(id)
		if request.method == 'GET': 
			return render_template('user/edit.html', logged_user=User.get_logged_user())
		else:
			user_name = request.form['user_name']
			password = request.form['password']
			role_id = request.form['role_id']
			image = user.image
			new_user = User(role_id, user_name, password, image)
			new_user.save()
			return redirect(url_for('show_users'))


	@app.route('/users/search', methods=['GET', 'POST'])
	def search_user():
		if request.method == 'GET': 
			return render_template('user/search.html', logged_user=User.get_logged_user())
		else:
			value = request.form['search_value']
			res = User.search(value)
			num_rows =  len(res)
			return render_template('user/search-results.html', value=value, results=res, 
					num_rows=num_rows, logged_user=User.get_logged_user())
		

	@app.route(f'/upload-image', methods=['GET', 'POST'])
	def upload_image():
		logged_user = User.get_logged_user_basic()
		if request.method == 'GET': 
			return render_template('user/upload-image.html', logged_user=logged_user)
		else:
			user_id = logged_user.user_id
			uploader = FileUploader()
			image = uploader.upload_image('image', UPLOAD_DIR_IMGS)
			logged_user.update_image(image, user_id)
			return redirect(url_for('get_user_data'))