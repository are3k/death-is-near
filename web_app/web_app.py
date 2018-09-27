from flask import Flask, render_template, redirect, flash
from config import Config
import sys, os
from forms import ModellForm
from model import *

web_app = Flask(__name__)

web_app.config.from_object(os.getenv('web_app_SETTINGS', 'config.Config'))


@web_app.route('/')
def index():
	form = ModellForm()
	modell = model.modell(none, 'kolonnevelger',verdi)
	return render_template('index.html', index=True, form=form, modell=modell)


@web_app.route('/about', methods=['GET','POST'])
def about():
	return render_template('about.html', about=True)


if __name__ == '__main__':
	web_app.run(host='0.0.0.0', debug=web_app.config['DEBUG'], port=web_app.config['PORT'])
