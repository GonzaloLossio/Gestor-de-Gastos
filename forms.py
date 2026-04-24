from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import length,equal_to,email,data_required,ValidationError
from models import User


class Registro(FlaskForm):

    def validate_username(self,username_to_check):
        username = User.query.filter_by(username=username_to_check.data).first()
        if username:
            raise ValidationError("Ya hay un usuario con este nombre registrado, prueba a registrar otro nombre de usuario!")
        
    def validate_email_adress(self,email_adress_to_check):
        email_adress = User.query.filter_by(email = email_adress_to_check.data).first()
        if email_adress:
            raise ValidationError("El correo electronico que ha puesto ya esta registrado,prueba a registrar otro correo electronico!") 


    username  = StringField(label='Nombre de Usuario',validators =[data_required(),length(min = 5, max=20)])
    email_adress = StringField(label='Correo Electronico', validators=[email(),data_required()])
    password1=PasswordField(label='Contraseña',validators = [data_required()])
    password2=PasswordField(label='Confirme La Contraseña', validators=[equal_to('password1'),data_required()])
    submit = SubmitField(label="Registrarse")

class Login(FlaskForm):
    email_adress = StringField(label='Correo Electronico', validators=[email(),data_required()])
    password=PasswordField(label='Contraseña',validators = [data_required()])
    submit = SubmitField(label="Iniciar Sesion")