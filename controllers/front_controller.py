from config import *
from flask import render_template

class FrontController:

	@app.route('/', methods=['GET'])
	def index():
		return render_template('front/index.html')

	@app.route('/register', methods=['GET'])
	def register():
		return render_template('front/index.html')