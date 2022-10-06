from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def valida_usuario(formulario):
        #formulario = DICCIONARIO con todos los names y valores que el usuario ingresa
        es_valido = True
        #Validamos que el nombre tenga al menos 3 caracteres
        if len(formulario['first_name']) < 3:
            flash('El nombre debe tener al menos 3 caracteres', 'registro')
            es_valido = False
        if len(formulario['last_name']) < 3:
            flash('El apellido debe tener al menos 3 caracteres', 'registro')
            es_valido = False
        if len(formulario['password']) < 3:
            flash('La contraseña debe tener al menos 6 caracteres', 'registro')
            es_valido = False
        #Verificamos que las contraseñas coincidan 
        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseñas NO coinciden', 'registro')
            es_valido = False
        #Revisamos que el email tenga el formato correcto -> Expresiones regulares
        if not EMAIL_REGEX.match(formulario['email']):
            flash('Email inválido', 'registro')
            es_valido = False
        #Consultamos si existe el correo electronico
        query = "SELECT * FROM users WHERE email =  %(email)s"
        results = connectToMySQL('recetas').query_db(query, formulario)
        if len(results) >= 1:
            flash('Email registrado previamente', 'registro')
            es_valido = False

        return es_valido

    @classmethod
    def save(cls,formulario):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s) "
        result = connectToMySQL('recetas').query_db(query, formulario)
        return result 

    @classmethod
    def get_by_email(cls, formulario):
        #formulario = {email: elena@coding.com, password: 3332423}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('recetas').query_db(query, formulario)# SELECT regresa siempre una lista, si no existe es una lista vacia, el usuario 0 es el que inicia sesion
        if len(result) < 1: #significa que mi lista está vacía entonces no existe ese email
            return False
        else:
            #me regresa una lista con 1 registro correspondiente al usuario de ese email
            #[
            # {id:1; email: ewewkjw, password: djkdwj}] tengo que transformarlo en instancia:
            user = cls(result[0])
            return user
    @classmethod
    def get_by_id(cls, formulario):
        #formulario: DICCIONARIO {id:3}
        query = "SELECT * FROM users where id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, formulario)
        user = cls(result[0]) #creamos una instancia de User
        return user
        
