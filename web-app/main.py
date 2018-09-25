from flask import Flask, render_template, redirect, flash
from config import Config
from db import Db
import sys, os
from forms import JobsForm

app = Flask(__name__)

app.config.from_object(os.getenv('APP_SETTINGS', 'config.Config'))

@app.route('/')
@app.route('/jobs')
def index():
	try:
		db = Db()
	except ValueError:
		e = sys.exc_info()
		return render_template('error.html',
			msg = "Database connection problem: " + str(e),
			errorTxt = "Contact system administrator")
	except:
		e = sys.exc_info()
		return render_template('error.html',
			msg = "Unknown database problems" + str(e),
			errorTxt = "Contact system administrator")
	try:
		cursor = db.fetch("select * from jobs")
		return render_template('index.html',
			data = cursor)
	except:
		e = sys.exc_info()
		return render_template('error.html',
			msg = "Database search problem: " + str(e))

@app.route('/planning', methods=['GET','POST'])
def planning():
	form = JobsForm()
	if form.validate_on_submit():
		flash('Job saved')
		return redirect('/')
	return render_template('jobsform.html', title='New job', data=str(app.config['PORT']), form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=app.config['PORT'])
