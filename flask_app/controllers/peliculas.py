
from flask import render_template, redirect, request, flash, session, url_for
from flask_app.models.pelicula import Pelicula
from flask_app.models.usuario import Usuario
from datetime import datetime
from flask_app import app

@app.route('/nueva_pelicula', methods=['GET', 'POST'])
def nueva_pelicula():
    if 'usuario_id' not in session:
        return redirect("/")
    if request.method == 'GET':
        return render_template('nuevo.html')
    
    if request.method == 'POST':
        data = {
            'pelicula': request.form['pelicula'],
            'fecha_inicio': request.form['fechaInicio'],
            'director' : request.form['director'],
            'sinopsis': request.form['sinopsis'],
            'id_organizador': session['usuario_id']
        }
        # Validar los datos
        errores = Pelicula.validar_pelicula(data)
        if errores:
            for error in errores:
                flash(error, 'error')
            return render_template('nuevo.html', data=data)
        # Crear el pelicula
        pelicula_id = Pelicula.crear(data)
        if pelicula_id:
            return redirect(url_for('dashboard'))
        flash('Error al crear el pelicula', 'error')
        return render_template('nuevo.html', data=data)

@app.route('/ver_pelicula/<int:id>')
def ver_pelicula(id):
    pelicula = Pelicula.obtener_por_id(id)
    if not pelicula:
        flash('pelicula no encontrado', 'error')
        return redirect(url_for('dashboard'))
    return render_template('ver_pelicula.html', pelicula=pelicula)

@app.route("/editar_pelicula/<int:id>")
def editar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect("/")
    pelicula = Pelicula.obtener_por_id(id)
    if pelicula.id_organizador != session['usuario_id']:
        flash("No tienes permiso para editar este pelicula", "error") 
        return redirect(url_for('dashboard'))
    else:
        return render_template("editar_pelicula.html", data=pelicula)

@app.route("/actualizar_pelicula", methods=['POST'])
def actualizar_pelicula():
    if 'usuario_id' not in session:
        return redirect("/")
    datos = {
        "id_pelicula": request.form['id_pelicula'],
        'pelicula': request.form['pelicula'],
        "fecha_inicio": request.form['fechaInicio'],
        "director": request.form['director'],
        "sinopsis": request.form['sinopsis'],
    }
    # Validación del pelicula
    errores = Pelicula.validar_pelicula(datos)
    if errores:
        for error in errores:
            flash(error, 'error')
        return render_template('editar_pelicula.html', data=datos)
    Pelicula.actualizar(datos)
    return redirect(url_for('dashboard'))

@app.route('/eliminar_pelicula/<int:id>')
def eliminar_pelicula(id):
    if Pelicula.eliminar(id):
        return redirect(url_for('dashboard'))