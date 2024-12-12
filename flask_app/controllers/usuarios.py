from flask_app import app
from flask import render_template, redirect,request,session, flash
from flask_app.models.usuario import Usuario
from flask_app.models.pelicula import Pelicula
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    peliculas = Pelicula.get_all()
    usuario = Usuario.get_by_id(session['usuario_id'])
    return render_template(
        "dashboard.html",
        peliculas=peliculas,
        usuario=usuario
    )

@app.route('/usuarios/registro', methods=['POST'])
def agregar_usuario():
    data = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirmar_password': request.form['confirmar_password']
    }
    if not Usuario.validar(data):
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'email': request.form['email'],
            'password': pw_hash
        }
        print(data)
        usuario_id = Usuario.save(data)
        session['usuario_id'] = usuario_id
        return redirect('/')

@app.route('/cerrar_sesion', methods = ['POST'])
def cerrar_sesion():
    session.clear()
    return redirect('/')

@app.route('/inicio/sesion', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario.get_by_email(request.form['loginEmail'])
        print(usuario)
        if usuario and bcrypt.check_password_hash(usuario.password, request.form['loginPassword']):
            session['usuario_id'] = usuario.id
            session['nombre'] = usuario.nombre
            return redirect('/dashboard')
        elif not usuario:
            print("Email inválido")
            flash("Email inválido", "login")
            return redirect('/')
        else:
            flash("Contraseña inválida", "login")
            return redirect('/')
    return redirect('/')

