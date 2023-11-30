from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

'''
Este código importa diferentes módulos y clases necesarios para el desarrollo de una aplicación Flask.

Flask: Es la clase principal de Flask, que se utiliza para crear instancias de la aplicación Flask.
jsonify: Es una función que convierte los datos en formato JSON para ser enviados como respuesta desde la API.
request: Es un objeto que representa la solicitud HTTP realizada por el cliente.
CORS: Es una extensión de Flask que permite el acceso cruzado entre dominios (Cross-Origin Resource Sharing), lo cual es útil cuando se desarrollan aplicaciones web con frontend y backend separados.
SQLAlchemy: Es una biblioteca de Python que proporciona una abstracción de alto nivel para interactuar con bases de datos relacionales.
Marshmallow: Es una biblioteca de serialización/deserialización de objetos Python a/desde formatos como JSON.
Al importar estos módulos y clases, estamos preparando nuestro entorno de desarrollo para utilizar las funcionalidades que ofrecen.

'''
'''
En este código, se está creando una instancia de la clase Flask y se está configurando para permitir el acceso cruzado entre dominios utilizando el módulo CORS.

app = Flask(__name__): Se crea una instancia de la clase Flask y se asigna a la variable app. El parámetro __name__ es una variable que representa el nombre del módulo o paquete en el que se encuentra este código. Flask utiliza este parámetro para determinar la ubicación de los recursos de la aplicación.

CORS(app): Se utiliza el módulo CORS para habilitar el acceso cruzado entre dominios en la aplicación Flask. Esto significa que el backend permitirá solicitudes provenientes de dominios diferentes al dominio en el que se encuentra alojado el backend. Esto es útil cuando se desarrollan aplicaciones web con frontend y backend separados, ya que permite que el frontend acceda a los recursos del backend sin restricciones de seguridad del navegador. Al pasar app como argumento a CORS(), se configura CORS para aplicar las políticas de acceso cruzado a la aplicación Flask representada por app.

'''
# Crea una instancia de la clase Flask con el nombre de la aplicación
app = Flask(__name__)
# Configura CORS para permitir el acceso desde el frontend al backend
CORS(app)

'''
En este código, se están configurando la base de datos y se están creando objetos para interactuar con ella utilizando SQLAlchemy y Marshmallow.

app.config["SQLALCHEMY_DATABASE_URI"]: Se configura la URI (Uniform Resource Identifier) de la base de datos. En este caso, se está utilizando MySQL como el motor de base de datos, el usuario y la contraseña son "root", y la base de datos se llama "proyecto". Esta configuración permite establecer la conexión con la base de datos.

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]: Se configura el seguimiento de modificaciones de SQLAlchemy. Al establecerlo en False, se desactiva el seguimiento automático de modificaciones en los objetos SQLAlchemy, lo cual mejora el rendimiento.

db = SQLAlchemy(app): Se crea un objeto db de la clase SQLAlchemy, que se utilizará para interactuar con la base de datos. Este objeto proporciona métodos y funcionalidades para realizar consultas y operaciones en la base de datos.

ma = Marshmallow(app): Se crea un objeto ma de la clase Marshmallow, que se utilizará para serializar y deserializar objetos Python a JSON y viceversa. Marshmallow proporciona una forma sencilla de definir esquemas de datos y validar la entrada y salida de datos en la aplicación. Este objeto se utilizará para definir los esquemas de los modelos de datos en la aplicación.

'''
# Configura la URI de la base de datos con el driver de MySQL, usuario, contraseña y nombre de la base de datos
# URI de la BD == Driver de la BD://user:password@UrlBD/nombreBD
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/proyecto"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/alumno_notas"
#anda con esto http://127.0.0.1:5000/alumnos

# Configura el seguimiento de modificaciones de SQLAlchemy a False para mejorar el rendimiento
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Crea una instancia de la clase SQLAlchemy y la asigna al objeto db para interactuar con la base de datos
db = SQLAlchemy(app)
# Crea una instancia de la clase Marshmallow y la asigna al objeto ma para trabajar con serialización y deserialización de datos
ma = Marshmallow(app)

class Alumnos(db.Model):  # Producto hereda de db.Model
    """
    Definición de la tabla en la base de datos.
    La clase Alumnos hereda de db.Model.
    Esta clase representa la tabla "Alumnos" en la base de datos.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))

    edad = db.Column(db.Integer)
    curso = db.Column(db.Integer)
    filosofia = db.Column(db.Integer)
    ingles = db.Column(db.Integer)
    fisica = db.Column(db.Integer)
    matematica = db.Column(db.Integer)
    musica = db.Column(db.Integer)
    literatura = db.Column(db.Integer)
    biologia = db.Column(db.Integer)
    quimica = db.Column(db.Integer)

    def __init__(self, nombre, edad, curso, filosofia, ingles, fisica, matematica, musica, literatura,
    biologia, quimica):
        """
        Constructor de la clase Alumnos
            
        """
        self.nombre = nombre
        self.edad = edad
        self.curso = curso
        self.filosofia = filosofia
        self.ingles = ingles
        self.fisica = fisica
        self.matematica = matematica
        self.musica = musica
        self.literatura = literatura
        self.biologia = biologia
        self.quimica = quimica



    # Se pueden agregar más clases para definir otras tablas en la base de datos

with app.app_context():
    db.create_all()  # Crea todas las tablas en la base de datos

# Definición del esquema para la clase Producto
class AlumnoSchema(ma.Schema):
    """
    Esquema de la clase Producto.

    Este esquema define los campos que serán serializados/deserializados
    para la clase Producto.
    """
    class Meta:
        fields = ("id", "nombre", "edad", "curso", "filosofia", "ingles", "fisica", "matematica", "musica", "literatura",
        "biologia", "quimica")

alumno_schema = AlumnoSchema()  # Objeto para serializar/deserializar un producto
alumnos_schema = AlumnoSchema(many=True)  # Objeto para serializar/deserializar múltiples productos

'''
Este código define un endpoint que permite obtener todos los productos de la base de datos y los devuelve como un JSON en respuesta a una solicitud GET a la ruta /productos.
@app.route("/productos", methods=["GET"]): Este decorador establece la ruta /productos para este endpoint y especifica que solo acepta solicitudes GET.
def get_Productos(): Esta es la función asociada al endpoint. Se ejecuta cuando se realiza una solicitud GET a la ruta /productos.
all_productos = Producto.query.all(): Se obtienen todos los registros de la tabla de productos mediante la consulta Producto.query.all(). Esto se realiza utilizando el modelo Producto que representa la tabla en la base de datos. El método query.all() heredado de db.Model se utiliza para obtener todos los registros de la tabla.
result = productos_schema.dump(all_productos): Los registros obtenidos se serializan en formato JSON utilizando el método dump() del objeto productos_schema. El método dump() heredado de ma.Schema se utiliza para convertir los objetos Python en representaciones JSON.
return jsonify(result): El resultado serializado en formato JSON se devuelve como respuesta al cliente utilizando la función jsonify() de Flask. Esta función envuelve el resultado en una respuesta HTTP con el encabezado Content-Type establecido como application/json.

'''
@app.route("/alumnos", methods=["GET"])
def get_Alumnos():
    all_alumnos = Alumnos.query.all()  # Obtiene todos los registros de la tabla
    result = alumnos_schema.dump(all_alumnos)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

@app.route("/alumnos/<id>", methods=["GET"])
def get_alumno(id):
    alumno = Alumnos.query.get(id)  # Obtiene el alumnocorrespondiente al ID recibido
    return alumno_schema.jsonify(alumno)  # Retorna el JSON del alumno

@app.route("/alumnos/<id>", methods=["DELETE"])
def delete_alumno(id):
    alumno = Alumnos.query.get(id)  # Obtiene el alumno correspondiente al ID recibido
    db.session.delete(alumno)  # Elimina el alumno de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return alumno_schema.jsonify(alumno)  # Retorna el JSON del alumno eliminado

@app.route("/alumnos", methods=["POST"]) 
def create_alumno():
    nombre = request.json["nombre"]  
    edad = request.json["edad"] 
    curso = request.json["curso"]
    filosofia = request.json["filosofia"]  
    ingles = request.json["ingles"]
    fisica = request.json["fisica"]
    matematica = request.json["matematica"]
    musica = request.json["musica"]
    literatura = request.json["literatura"]
    biologia = request.json["biologia"]
    quimica = request.json["quimica"]

    new_alumno = Alumnos(nombre, edad, curso, filosofia, ingles, fisica, matematica, musica, literatura,
    biologia, quimica)  

    db.session.add(new_alumno)  
    db.session.commit()  # Guarda los cambios en la base de datos
    return alumno_schema.jsonify(new_alumno)  # Retorna el JSON del nuevo alumno

@app.route("/alumnos/<id>", methods=["PUT"])  # Endpoint para actualizar 
def update_alumno(id):
    alumno = Alumnos.query.get(id)  # Obtiene el existente con el ID especificado

    # Actualiza los atributos del producto con los datos proporcionados en el JSON
    alumno.nombre = request.json["nombre"]  
    alumno.edad = request.json["edad"] 
    alumno.curso = request.json["curso"]
    alumno.filosofia = request.json["filosofia"]  
    alumno.ingles = request.json["ingles"]
    alumno.fisica = request.json["fisica"]
    alumno.matematica = request.json["matematica"]
    alumno.musica = request.json["musica"]
    alumno.literatura = request.json["literatura"]
    alumno.biologia = request.json["biologia"]
    alumno.quimica = request.json["quimica"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return alumno_schema.jsonify(alumno)  # Retorna el JSON del producto actualizado

'''
Este código es el programa principal de la aplicación Flask. Se verifica si el archivo actual está siendo ejecutado directamente y no importado como módulo. Luego, se inicia el servidor Flask en el puerto 5000 con el modo de depuración habilitado. Esto permite ejecutar la aplicación y realizar pruebas mientras se muestra información adicional de depuración en caso de errores.

'''
# Programa Principal
if __name__ == "__main__":
    # Ejecuta el servidor Flask en el puerto 5000 en modo de depuración
    app.run(debug=True, port=5000)