import os
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Clave secreta para tokens CSRF (toma la variable de entorno o usa la predeterminada)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-secreta-mileni-store-2026')

# Configuración de la Base de Datos PostgreSQL
db_url = os.environ.get('DATABASE_URL', 'sqlite:///clientes.db')
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo seguro de la tabla de Clientes (ORM previene SQL Injection)
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    empresa = db.Column(db.String(100), nullable=True)
    notas = db.Column(db.Text, nullable=True)

# Crea la estructura de tablas automáticamente
with app.app_context():
    db.create_all()

# Formulario WTForms con validaciones estrictas y token CSRF automático
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
    mensaje = None

    # validate_on_submit() valida la autenticidad del token CSRF y los tipos de datos
    if form.validate_on_submit():
        nuevo_cliente = Cliente(
            nombre=form.nombre.data.strip(),
            correo=form.correo.data.strip(),
            telefono=form.telefono.data.strip(),
            empresa=form.empresa.data.strip() if form.empresa.data else None,
            notas=form.notas.data.strip() if form.notas.data else None
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        
        mensaje = "¡Cliente registrado y guardado de forma segura en la base de datos!"
        form = FormularioCliente(formdata=None)

    # Consulta segura de todos los clientes registrados
    lista_clientes = Cliente.query.order_by(Cliente.id.desc()).all()

    return render_template('index.html', form=form, clientes=lista_clientes, mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=False)
