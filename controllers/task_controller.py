from config import *
from models.user import User
from models.task import Task
from flask import render_template, request, redirect, url_for, session

class TaskController:


	@app.route('/tasks', methods=['GET'])
	def show_tasks():
		tasks = Task.get_all_data()
		num_rows = len(tasks)
		return render_template('task/show.html', tasks=tasks, num_rows=num_rows, logged_user=User.get_logged_user())


	@app.route('/my-tasks', methods=['GET'])
	def user_tasks():
		logged_user=User.get_logged_user()
		tasks = Task.get_all_user_tasks(logged_user.user_id)
		num_rows = len(tasks)
		return render_template('task/user-tasks.html', tasks=tasks, num_rows=num_rows, logged_user=logged_user)


	@app.route('/tasks/<id>/details', methods=['GET'])
	def task_details(id):
		task = Task.get_data_by_id(id)
		if task:
			return render_template('task/details.html', task=task, logged_user=User.get_logged_user())
		else:
			return render_template('errorr/404.html')


	@app.route('/tasks/add', methods=['GET', 'POST'])
	def add_task():
		logged_user=User.get_logged_user()
		if request.method == 'GET': 
			return render_template('task/add.html', logged_user=logged_user)
		else:
			task_name = request.form['task_name']
			start_date = request.form['start_date']
			end_date = request.form['end_date']
			description = request.form['description']
			user_id = logged_user.user_id
			task = Task(user_id, task_name, start_date, end_date, description)
			task.save()
			return redirect(url_for('user_tasks'))


	@app.route('/tasks/<id>/edit', methods=['GET', 'POST'])
	def edit_task(id):
		task = Task.get_by_id(id)
		logged_user=User.get_logged_user()
		if request.method == 'GET': 
			return render_template('task/edit.html', task=task, logged_user=logged_user)
		else:
			task_name = request.form['task_name']
			start_date = request.form['start_date']
			end_date = request.form['end_date']
			description = request.form['description']
			user_id = logged_user.user_id
			new_task = Task(user_id, task_name, start_date, end_date, description)
			new_task.save()
			return redirect(url_for('show_users'))


	@app.route('/task/search', methods=['GET', 'POST'])
	def search_task():
		if request.method == 'GET': 
			return render_template('task/search.html',logged_user=User.get_logged_user())
		else:
			value = request.form['search_value']
			res = Task.search(value)
			num_rows =  len(res)
			return render_template('task/search-results.html', value=value, results=res, 
					num_rows=num_rows, logged_user=User.get_logged_user())