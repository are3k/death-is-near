from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class JobsForm(FlaskForm):
    job_name = StringField('Job name', validators=[DataRequired()])
    job_description = StringField('Description')
    submit = SubmitField('Apply')