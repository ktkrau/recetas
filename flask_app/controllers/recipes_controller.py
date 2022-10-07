from flask import render_template, redirect, session, request
from flask_app import app
#modelos
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

@app.route('/new/recipe')
def new_recipe():
    #necesito que el usuario ya haya iniciado sesion y el nombre
    if 'user_id' not in session:
        return redirect('/')
    #Yo sé que en sesión tengo el id de mi usuario(sesson[user_id])
    #Queremos una funcion que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session["user_id"]}

    user = User.get_by_id(formulario)

    return render_template('new_recipe.html', user=user)

@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')
    
    #Validación de Receta
    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe')
    
    #Guardamos la receta
    Recipe.save(request.form)

    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session: #comprobamos que inicia sesion
        return redirect('/')
    #Yo sé que en sesión tengo el id de mi usuario(sesson[user_id])
    #Queremos una funcion que en base a ese id me regrese una instancia del usuario // no se cual es el nombre del usuario
    formulario = {"id": session["user_id"]}

    user = User.get_by_id(formulario) #recibo la instancia de usuario en base a su id para ver el nombre de usuario

    #la instancia de la receta que se debe desplegar en editar - en base al id que recibimos en su URL
    formulario_receta = {"id": id}
    recipe = Recipe.get_by_id(formulario_receta)


    return render_template('edit_recipe.html', user=user, recipe = recipe)


@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    #verificar que haya iniciado sesion
    if 'user_id' not in session: #comprobamos que inicia sesion
        return redirect('/')
    #recibimos formulario = request.form
    #{name: Albondigas, description: "bolitas de carne, instructions...., recipe_id : 1"}

    #verificar que todos los datos estén correctos
    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['recipe_id']) #edit/recipe/1

    #guardar los cambios
    Recipe.update(request.form)

    #redireccionar a /dashboard
    return redirect('/dashboard')

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    #verificar que haya iniciado sesión
    if 'user_id' not in session: #comprobamos que inicia sesion
        return redirect('/')
    #borramos
    formulario = {"id": id}
    Recipe.delete(formulario)
    
    #redirigir a /dashboard
    return redirect('/dashboard')

@app.route('/view/recipe/<int:id>')
def view_recipe(id):
    #verificar inicio de sesión
    if 'user_id' not in session:
        return redirect('/')

    #saber cual es el nombre del usuario que inicio sesión
    formulario = {"id": session["user_id"]}

    user = User.get_by_id(formulario)

    #objeto receta a desplegar
    formulario_receta = {"id":id}
    recipe = Recipe.get_by_id(formulario_receta)
    #renderizar show_recipe.html
    return render_template('show_recipe.html', user=user, recipe=recipe)

