from flask import Flask, render_template, redirect, flash
from config import Config
import sys, os
from forms import ModellForm
import model

web_app = Flask(__name__)

web_app.config.from_object(os.getenv('web_app_SETTINGS', 'config.Config'))


@web_app.route('/', methods=['GET','POST'])
def index():
	form = ModellForm()
	if form.validate_on_submit():
		modell = model.modell(form.change_parameter.data,
			form.change.data)
		return render_template('index.html',
			index=True,
			form=form,
			change_parameter=form.change_parameter.data)
	#modell = model.modell(none, 'kolonnevelger',verdi)
	#modell = model.reality()
	return render_template('index.html', index=True, form=form)


@web_app.route('/about')
def about():
	return render_template('about.html', about=True)


if __name__ == '__main__':
	web_app.run(host='0.0.0.0', debug=web_app.config['DEBUG'], port=web_app.config['PORT'])
