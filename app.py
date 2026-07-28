import os
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)

# Clave secreta requerida para tokens CSRF (Usa una variable de entorno o una clave fuerte)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-secreta-de-prueba-mileni-2026')

# Definición del formulario con validaciones de seguridad incorporadas
class FormularioCliente(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=3, max=80, message="El nombre debe tener entre 3 y 80 caracteres.")
    ])
    correo = StringField('Correo Electrónico', validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Ingresa un correo electrónico válido."),
        Length(max=120)
    ])
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El teléfono es obligatorio."),
        Length(min=7, max=20, message="Ingresa un número de teléfono válido.")
    ])
    empresa = StringField('Empresa / Negocio', validators=[
        Length(max=100)
    ])
    notas = TextAreaField('Detalle del Servicio / Notas', validators=[
        Length(max=500, message="Las notas no pueden superar los 500 caracteres.")
    ])
    submit = SubmitField('Guardar Cliente')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FormularioCliente()
    cliente = None
    mensaje = None

    # validate_on_submit verifica los datos y el token CSRF automáticamente
    if form.validate_on_submit():
        cliente = {
            'nombre': form.nombre.data.strip(),
            'correo': form.correo.data.strip(),
            'telefono': form.telefono.data.strip(),
            'empresa': form.empresa.data.strip(),
            'notas': form.notas.data.strip()
        }
        mensaje = "¡Cliente registrado con éxito y datos validados de forma segura!"
        form = FormularioCliente(formdata=None) # Limpia el formulario tras el envío exitoso

    return render_template('index.html', form=form, cliente=cliente, mensaje=mensaje)

if __name__ == '__main__':
    # Mantenemos debug=False para garantizar la seguridad en producción
    app.run(debug=False)
