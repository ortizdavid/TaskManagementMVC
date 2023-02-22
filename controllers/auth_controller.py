from config import *
from helpers.password_handler import *
from models.user import User
from flask import render_template, request, redirect, url_for, session

class AuthController:

	@app.route('/login', methods=['GET', 'POST'])
	def login():
		if request.method == 'GET':
			return render_template('auth/login.html')
		else:
			user_name = request.form['user_name']
			password = request.form['password']
			user = User.get_by_username(user_name)

			encrypted_password = user.password
			if PasswordHandler.check(encrypted_password, password):
				session['user_name'] = user_name
				session['password'] = encrypted_password
				return redirect(url_for('home'))
			else:
				return redirect(url_for('login'))


	@app.route('/logout', methods=['GET'])
	def logout():
		session.pop('user_name')
		return redirect(url_for('login'))


	@app.route('/home', methods=['GET'])
	def home():
		return render_template('auth/home.html', logged_user=User.get_logged_user())