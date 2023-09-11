from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length

# Classe de formulário de login
class LoginForm(FlaskForm):
  username = StringField('CPF',
                         validators=[DataRequired(),
                                     Length(min=11, max=11)])

  password = PasswordField('Senha',
                           validators=[DataRequired(),
                                       Length(min=5, max=20)])
  submit = SubmitField('Login')


# Classe de formulário de cadastro
class RegistrationForm(FlaskForm):
  username = StringField('CPF',
                         validators=[DataRequired(),
                                     Length(min=11, max=11)])
  name = StringField('Nome', validators=[DataRequired()])
  password = PasswordField('Senha',
                           validators=[DataRequired(),
                                       Length(min=5, max=20)])
  password2 = PasswordField('Confirma a Senha',
                            validators=[DataRequired(),
                                        Length(min=5, max=20)])
  submit = SubmitField('Register')
