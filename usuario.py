from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def guardar(cls, data):
        query = "INSERT INTO usuarios (nombre, apellido, email, password, created_at, updated_at) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('certificacion_02').query_db(query, data)

    @classmethod
    def obtener_por_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL('certificacion_02').query_db(query, {'email': email})
        # si no encuentra el correo devuelve False
        if len(resultado) < 1:
            return False
        return cls(resultado[0])

    @staticmethod
    def validar_registro(formulario):
        es_valido = True

        if len(formulario['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteres", "registro")
            es_valido = False
        if len(formulario['apellido']) < 2:
            flash("El apellido debe tener al menos 2 caracteres", "registro")
            es_valido = False
        if not EMAIL_REGEX.match(formulario['email']):
            flash("E-mail inválido", "registro")
            es_valido = False
        elif Usuario.obtener_por_email(formulario['email']):
            flash("Ese e-mail ya está registrado", "registro")
            es_valido = False
        if len(formulario['password']) < 1:
            flash("La contraseña es obligatoria", "registro")
            es_valido = False
        elif formulario['password'] != formulario['conf_password']:
            flash("Las contraseñas no coinciden", "registro")
            es_valido = False

        return es_valido
