from flask_wtf import FlaskForm
from wtforms import FloatField, PasswordField, StringField, IntegerField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, Length, Email

class user_form(FlaskForm):
    username = StringField("User Name", validators=[InputRequired(message="Please enter a valid user name."), Length(max=20,message="username must be 20 characters or less")])
    email = StringField("Email", validators=[InputRequired(message="Please enter a valid email"), Length(max=50,message="email must be 50 characters or less"), Email(message="Please enter a valid email")])
    password = PasswordField("Password", validators=[InputRequired(message="Please enter a valid password"),Length(min=6,max=30,message="password must be between 6 and 30 characters long")])
    first_name = StringField("First Name", validators=[InputRequired(message="Please enter a valid name"),Length(max=30,message="first name must be 30 characters or less")])
    last_name = StringField("Last Name", validators=[InputRequired(message="Please enter a valid name"),Length(max=30,message="last name must be 30 characters or less")])
    submit = SubmitField("Add User")

class login_form(FlaskForm):
    username = StringField("User Name", validators=[InputRequired(message="Please enter a valid user name."), Length(max=20,message="username must be 20 characters or less")])
    password = PasswordField("Password", validators=[InputRequired(message="Please enter a valid password"),Length(min=6,max=30,message="password must be between 6 and 30 characters long")])
    submit = SubmitField("Login")

class new_feedback_form(FlaskForm):
    title = StringField("Title",validators=[InputRequired(message="Please enter a valid title."), Length(max=100,message="Title must be 100 characters or less")])
    content = StringField("Your Feedback",validators=[InputRequired(message="Please enter valid content.")])
    submit = SubmitField("Add Feedback")

class update_feedback_form(FlaskForm):
    title = StringField("Title",validators=[InputRequired(message="Please enter a valid title."), Length(max=100,message="Title must be 100 characters or less")])
    content = StringField("Your Feedback",validators=[InputRequired(message="Please enter valid content.")])
    submit = SubmitField("Edit Feedback")