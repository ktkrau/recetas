from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        #LEFT JOIN
        self.first_name = data['first_name']

    
    @staticmethod
    def valida_receta(formulario):
        es_valido = True

        if len(formulario['name']) < 3:
            flash('El nombre de la receta debe tener al menos 3 caracteres', 'receta')
            es_valido = False
        
        if len(formulario['description']) < 3:
            flash('La descripción de la receta debe tener al menos 3 caracteres', 'receta')
            es_valido = False

        if len(formulario['instructions']) < 3:
            flash('Las instrucciones de la receta debe tener al menos 3 caracteres', 'receta')
            es_valido = False
        
        if formulario['date_made'] == '':
            flash('Ingrese una fecha', 'receta')
            es_valido = False

        return es_valido


    #funcion para guardar recetas

    @classmethod
    def save(cls, formulario):
        #formulario = {name: "albondigas", description: "albondigas vegetarianas", instructions:"......".....}
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s)"
        results = connectToMySQL('recetas').query_db(query, formulario)
        return results
        
        
    #query que seleccione todas las columnas de recetas y aparte el nombre de la persona que la creó

    @classmethod
    def get_all(cls):
        query = "select recipes.*, first_name from recipes LEFT JOIN users ON users.id = recipes.user_id"
        results = connectToMySQL('recetas').query_db(query) #Lista de muchos Diccionarios
        recipes = []

        for recipe in results:
            #recipe = diccionario{}
            recipes.append(cls(recipe))#1.- en cls(recipe) creamos la instancia en base al diccionario 2.- gracias al recipe.append agrego eso instancia a la lista vacia recipes

        return recipes


    @classmethod
    def get_by_id(cls, formulario):
        #formulario : diccionario con el identificador de mi usuario = {id: 1}
        query = "select recipes.*, first_name from recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, formulario) #recibimos una lista con un diccionario
        #quiero regresar un objeto de receta:
        recipe = cls(result[0]) #la posicion 0 es la que quiero transformar en objeto de receta, cls()(se crea la instancia en base a ese diccionario)
        return recipe

    @classmethod
    def update(cls, formulario):
        #formulario = {name: Albondigas, description: "bolitas de carne, instructions...., recipe_id : 1"}
        query = "UPDATE recipes SET name = %(name)s, description=%(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s WHERE id = %(recipe_id)s"
        result = connectToMySQL('recetas').query_db(query, formulario) 
        return result

    @classmethod
    def delete(cls, formulario):
        #formulario = diccionario {id: 1}
        query = "DELETE FROM recipes WHERE id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, formulario)
        return result



    






        

        











