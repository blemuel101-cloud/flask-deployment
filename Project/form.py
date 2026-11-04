from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 2, max = 5)])

    password = StringField('Password', validators=[DataRequired(), Length(min = 2, max = 20)])

    submit = SubmitField('Submit')
