from flask import render_template, redirect, request, session, flash
from flask_app import app

from flask_app.models.users import User
from flask_bcrypt import Bcrypt
from flask_app.models.recipes import Recipe

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    #validamos la info que recibimos
    if not User.valida_usuario(request.form):
        return redirect('/')

    #guardar registro
    pwd = bcrypt.generate_password_hash(request.form['password'])#encriptar la contraseña del usuario y guardandola en pwd

    #creamos un diccionario con todos los datos del request.form:
    formulario = {
        "first_name" : request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario) #recibir el identificador del nuevo usuario

    session['user_id'] = id #guardamos en session el identificador del usuario
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    #verificamos que el email exista en la base de datos
    user = User.get_by_email(request.form) #1.Recibimos falso 2. recibimos una instancia de usuario
    if not user: #si user es = a falso
        flash('E-mail no encontrado', 'login')
        return redirect('/')

    #user es una instancia con todos los datos de mi usuario
    #como verificamos que el password está correcto o no: check_password_hash // funcion de bcrypt
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'login')
        return redirect('/')

    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    #Yo sé que en sesión tengo el id de mi usuario(sesson[user_id])
    #Queremos una funcion que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session["user_id"]}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su id

    #queremos recibir una lista con todas las recetas:
    recipes = Recipe.get_all()

    return render_template('dashboard.html', user = user, recipes=recipes)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

