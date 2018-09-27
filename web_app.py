from flask import Flask, render_template, redirect, flash
from web_app.config import Config
#from db import Db
import sys, os
from web_app.forms import JobsForm

web_app = Flask(__name__)

web_app.config.from_object(os.getenv('web_app_SETTINGS', 'config.Config'))

@web_app.route('/')
@web_app.route('/jobs')
def index():
	return render_template('index.html')
@web_app.route('/planning', methods=['GET','POST'])
def planning():
	form = JobsForm()
	if form.validate_on_submit():
		flash('Job saved')
		return redirect('/')
	return render_template('jobsform.html', title='New job', data=str(web_app.config['PORT']), form=form)

if __name__ == '__main__':
    web_app.run(host='0.0.0.0', debug=web_app.config['DEBUG'], port=web_app.config['PORT'])
