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
        self.image = data['image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        #LEFT JOIN
        self.first_name = data['first_name']

    @staticmethod
    def valida_receta(formulario):
        is_valid = True

        if len(formulario['name']) < 3:
            flash('El nombre de la receta debe tener al menos 3 caracteres', 'receta')
            is_valid = False
        
        if len(formulario['description']) < 3:
            flash('La descripción de la receta debe tener al menos 3 caracteres', 'receta')
            is_valid = False

        if len(formulario['instructions']) < 3:
            flash('Las instrucciones de la receta debe tener al menos 3 caracteres', 'receta')
            is_valid = False
        
        if len(formulario['date_made']) == '':
            flash('Ingrese la fecha', 'receta')
            is_valid = False

        return is_valid

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id, image) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s, %(image)s)"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT recipes.*, first_name FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL('esquema_recetas').query_db(query) #Lista de Diccionarios
        recipes = []

        for recipe in results:
            #recipe = diccionario
            recipes.append(cls(recipe)) #1.- cls(recipe) creamos la instancia en base al diccionario, 2.- recipes.append agrego esa instancia a la lista recipes
        
        return recipes

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT recipes.*, first_name FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario) # Cuando hacemos un SELECT recibimos una lista con un diccionario adentro
        recipe = cls(result[0]) #se transforma la intancia a un objeto de receta
        return recipe

    @classmethod
    def update(cls, formulario):
        #formulario = {name: Albondigas, description: bolitas de carne, instructions:......., recipe_id: 1}
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under_30=%(under_30)s WHERE id=%(id)s "
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario):
        query = "DELETE FROM recipes WHERE id =%(id)s"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        return result