from config import *
from flask import jsonify, render_template
from controllers import (
	user_controller,
	auth_controller,
	task_controller,
	front_controller
)

if __name__ == '__main__':
    app.run(port=APP_PORT, debug=True)