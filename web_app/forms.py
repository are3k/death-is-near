from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

class ModellForm(FlaskForm):
    change_parameter = SelectField(
        'Testparameter',
        choices=[('tm', 'Trafikkmengde'), ('fd', 'Fartsdempere'),
         ('atk', 'Fotoboks'), ('fg','Fartsgrense'), ('vb','Vegbredde')]
    )
    change = StringField('Endring')
    submit = SubmitField('Kjør modell')