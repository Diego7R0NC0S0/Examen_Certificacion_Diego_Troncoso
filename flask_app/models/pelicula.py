# modelos/pelicula.py
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask import flash

DATABASE = 'esquema_cinepedia'

class Pelicula:
    def __init__(self, data):
        self.id_pelicula = data['id_pelicula']
        self.pelicula = data['pelicula']
        self.fecha_inicio = data['fecha_inicio']
        self.director = data['director']
        self.sinopsis = data['sinopsis']
        self.id_organizador = data['id_organizador']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.organizador = data.get('organizador', None) 

    @classmethod
    def get_all(cls):
        query = """
            SELECT peliculas.id_pelicula, peliculas.*, usuarios.nombre AS organizador 
            FROM peliculas
            JOIN usuarios ON peliculas.id_organizador = usuarios.id
            ORDER BY peliculas.fecha_inicio;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        peliculas = []
        if results:
            for row in results:
                peliculas.append(cls(row))
        return peliculas

    @classmethod
    def crear(cls, data):
        query = """
            INSERT INTO peliculas (pelicula, fecha_inicio, director, sinopsis, id_organizador)
            VALUES (%(pelicula)s, %(fecha_inicio)s, %(director)s, %(sinopsis)s, %(id_organizador)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    # Método para validar los datos del pelicula
    @staticmethod
    def validar_pelicula(data):
        errores = []
        if len(data['pelicula']) < 3:
            errores.append("La película debe tener al menos 3 caracteres")
        
        if len(data['director']) < 3:
            errores.append("El campo director debe tener al menos 3 caracteres")
        
        if len(data['sinopsis']) < 3:
            errores.append("la sinopsis debe tener al menos 3 caracteres")
        
        if not data['fecha_inicio']:
            errores.append("La fecha de inicio no puede estar vacía")
        
        if not data['director']:
            errores.append("El director no puede estar vacío")
        
        if not data['sinopsis']:
            errores.append("sinopsis no puede estar vacía")
        
        if len(data['sinopsis']) > 40:
            errores.append("El sinopsis no puede tener más de 40 caracteres")
        # Validar fechas
        fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%dT%H:%M')
        if fecha_inicio <= datetime.now():
            errores.append("La fecha de inicio debe ser una fecha futura")
        return errores

    @classmethod
    def obtener_por_id(cls, id_pelicula):
        query = """
            SELECT peliculas.*, usuarios.nombre AS organizador 
            FROM peliculas
            JOIN usuarios ON peliculas.id_organizador = usuarios.id
            WHERE peliculas.id_pelicula = %(id_pelicula)s;
        """
        data = {'id_pelicula': id_pelicula}
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0]) if results else None

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE peliculas 
            SET pelicula = %(pelicula)s,
                fecha_inicio = %(fecha_inicio)s,
                director = %(director)s,
                sinopsis = %(sinopsis)s
            WHERE id_pelicula = %(id_pelicula)s;
        """
        
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def eliminar(cls, id_pelicula):
        query = "DELETE FROM peliculas WHERE id_pelicula = %(id_pelicula)s;"
        data = {'id_pelicula': id_pelicula}
        connectToMySQL(DATABASE).query_db(query, data)
        return True