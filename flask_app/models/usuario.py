from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOMBRE_REGEX = re.compile(r'[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.{8,})[a-zA-Z]+$')

DATABASE = 'esquema_cinepedia'

class Usuario:
    db_schema = 'esquema_cinepedia' 
    def __init__(self,data):
        self.id = data['id'] 
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "select * from usuarios;" 
        resultados = connectToMySQL(DATABASE).query_db(query)
        usuarios = [] 
        for usuario in resultados:
            usuarios.append(cls(usuario))
        return usuarios

    @classmethod
    def save(cls,data):
        query = "insert into usuarios (nombre, apellido, email, password) values (%(nombre)s, %(apellido)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultado = connectToMySQL(DATABASE).query_db(query, {'id': id})
        if not resultado:
            return False
        return cls(resultado[0])

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL(DATABASE).query_db(query, {'email': email})
        if len(resultado) < 1:
            return False
        return cls(resultado[0])

    @staticmethod
    def validar(data):
        is_valid = True
        query = "select * from usuarios where email=%(email)s;"
        resultado_query = connectToMySQL(Usuario.db_schema).query_db(query,data)
        if len(resultado_query)>0:
            flash("el email ya esta registrado", "registro")
            is_valid = False
        if len(data['nombre']) <2 : 
            flash("El nombre debe tener mas de 2 letras", "registro")
            is_valid = False
        if len(data['nombre']) <= 0:
            flash("El nombre no puede estar vacío.", "registro")
            is_valid = False
        if not NOMBRE_REGEX.match(data['nombre']):
            flash("El nombre no puede tener numeros o cracteres especiales","registro")
            is_valid = False
        if len(data['apellido']) <2:
            flash("El apellido debe de tener mas de 2 letras", "registro")
            is_valid = False
        if len(data['apellido']) <= 0:
            flash("El apellido no puede estar vacío.", "registro")
            is_valid = False
        if not NOMBRE_REGEX.match(data['apellido']):
            flash("El apellido no puede tener numeros o caracteres especiales","registro")
        if len(data['email']) <= 0:
            flash("El email no puede estar vacío.", "registro")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("El email no cumple con las caracteristicas minimas solicitadas","registro")
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash("La password no cumple con las cracteristicas minimas requeridas", "registro")
            is_valid = False
        if data['password'] != data['confirmar_password']:
            flash("La contraseña no coincide ", "registro")
            is_valid = False 
        if len(data['password'])<8:
            flash("la contraseña debe tener al menos 8 caracteres" , "registro")
        return is_valid


