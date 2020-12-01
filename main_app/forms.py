from flask_wtf import FlaskForm as Form
from wtforms import StringField,PasswordField,SubmitField,HiddenField
from wtforms.validators import DataRequired,Email,ValidationError,Length,EqualTo
from main_app.models import User



class SignupForm(Form):
    username=StringField("Username",validators=[DataRequired(),Length(min=2)])
    name = StringField("Name",validators=[DataRequired(),Length(min=6,max=20)])
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired(),Length(min=4,max=12,message="Password should be of 4 to 12 characters")])
    confirm=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password',"Invalid confirm password!!")])
    submit=SubmitField("Sign Up")

    def validate_email(self,email):
      user=User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError("This Email is taken.Try a new One")


class LoginForm(Form):
    username=StringField("Username",validators=[DataRequired(),Length(min=2)])
    email=StringField("Email",validators=[DataRequired(),Email(message="Please check your email")])
    password=PasswordField("Password",validators=[DataRequired(),Length(min=4,max=12,message="Password should be of 4 to 12 characters")])
    submit=SubmitField("Login")

