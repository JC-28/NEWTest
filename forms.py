from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email


class SignUp(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    email = StringField('Please enter email: eg; bob@bob.com', validators= [InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    submit = SubmitField('Sign Up', render_kw={'class': 'submitBtn'})


class LogIn(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn'})


#for recipe?
