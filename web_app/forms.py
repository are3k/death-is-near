from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

class ModellForm(FlaskForm):
    change_parameter = SelectField(
        'Testparameter',
        choices=[('trafikk_mengde', 'Trafikkmengde'),
         ('fartsdempere', 'Fartsdempere'),
         ('fotobokser', 'Fotoboks'),
         ('fartsgrense','Fartsgrense'),
         ('svingerestriksjon','Svingrestriksjoner'),
         ('vilt_fare', 'Viltfare')]
    )
    change = StringField('Endring')
    submit = SubmitField('Kjør modell')