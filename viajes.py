from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.viaje import Viaje

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('dashboard.html', viajes=Viaje.obtener_todos())

@app.route('/nuevo')
def nuevo():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('nuevo_viaje.html', viaje={})

@app.route('/crear', methods=['POST'])
def crear():
    if 'usuario_id' not in session:
        return redirect('/')

    if not Viaje.validar_viaje(request.form):
        # vuelvo a mostrar el form con lo que ya habia escrito
        return render_template('nuevo_viaje.html', viaje=request.form)

    data = {
        'destino': request.form['destino'],
        'fecha_inicio': request.form['fecha_inicio'],
        'fecha_fin': request.form['fecha_fin'],
        'itinerario': request.form['itinerario'],
        'usuario_id': session['usuario_id']
    }
    Viaje.guardar(data)
    return redirect('/dashboard')

@app.route('/ver/<int:id>')
def ver(id):
    if 'usuario_id' not in session:
        return redirect('/')

    viaje = Viaje.obtener_por_id(id)
    if not viaje:
        return redirect('/dashboard')

    viajeros = Viaje.obtener_viajeros(id)
    # reviso si el usuario ya esta en la lista para mostrar Unirme o Cancelar
    inscrito = False
    for viajero in viajeros:
        if viajero['id'] == session['usuario_id']:
            inscrito = True

    return render_template('ver_viaje.html', viaje=viaje, viajeros=viajeros, inscrito=inscrito)

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_id' not in session:
        return redirect('/')

    viaje = Viaje.obtener_por_id(id)
    # solo el que creo el viaje lo puede editar
    if not viaje or viaje.usuario_id != session['usuario_id']:
        return redirect('/dashboard')

    return render_template('editar_viaje.html', viaje=viaje, id=id)

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    if 'usuario_id' not in session:
        return redirect('/')

    viaje = Viaje.obtener_por_id(id)
    if not viaje or viaje.usuario_id != session['usuario_id']:
        return redirect('/dashboard')

    if not Viaje.validar_viaje(request.form):
        return render_template('editar_viaje.html', viaje=request.form, id=id)

    data = {
        'id': id,
        'destino': request.form['destino'],
        'fecha_inicio': request.form['fecha_inicio'],
        'fecha_fin': request.form['fecha_fin'],
        'itinerario': request.form['itinerario']
    }
    Viaje.actualizar(data)
    return redirect('/dashboard')

@app.route('/borrar/<int:id>')
def borrar(id):
    if 'usuario_id' not in session:
        return redirect('/')

    viaje = Viaje.obtener_por_id(id)
    if viaje and viaje.usuario_id == session['usuario_id']:
        Viaje.eliminar(id)
    return redirect('/dashboard')

@app.route('/unirme/<int:id>', methods=['POST'])
def unirme(id):
    if 'usuario_id' not in session:
        return redirect('/')

    # para no insertar dos veces al mismo usuario (la bd no lo deja)
    viajeros = Viaje.obtener_viajeros(id)
    for viajero in viajeros:
        if viajero['id'] == session['usuario_id']:
            return redirect(f'/ver/{id}')

    Viaje.unirse({'usuario_id': session['usuario_id'], 'viaje_id': id})
    return redirect(f'/ver/{id}')

@app.route('/cancelar/<int:id>', methods=['POST'])
def cancelar(id):
    if 'usuario_id' not in session:
        return redirect('/')

    Viaje.cancelar({'usuario_id': session['usuario_id'], 'viaje_id': id})
    return redirect(f'/ver/{id}')
