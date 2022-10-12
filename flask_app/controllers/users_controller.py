from flask import render_template, redirect, request, session, flash, jsonify
from flask_app import app

#Importamos Modelo
from flask_app.models.users import User
from flask_app.models.recipes import Recipe


#Importación de Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.valida_usuario(request.form):
        return redirect('/')
    pwd = bcrypt.generate_password_hash(request.form['password']) #Encriptando la contraseña del usuario y guardándola en pwd
    # request.form['password']= pwd
    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }
    id =User.save(formulario)

    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    #Verificamos que el email exista en la Base de datos
    user = User.get_by_email(request.form) #Recibimos una instancia de usuario O False

    if not user: #Si user = False
        # flash('E-mail no encontrado', 'login')
        # return redirect('/')
        return jsonify(menssage="E-mail no encontrado")

    #user es una instancia con todos los datos de mi usuario
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        # flash('Password incorrecto', 'login')
        # return redirect('/')
        return jsonify(message="Password incorrecto")

    session['user_id'] = user.id
    # return redirect('/dashboard')
    return jsonify(message="correcto")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        # 
        return jsonify(menssage="correcto")

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID
    recipes = Recipe.get_all()
        #RECIBIR UNA LISTA CON TODAS MIS RECETAS
    return render_template('dashboard.html', user=user, recipes=recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


