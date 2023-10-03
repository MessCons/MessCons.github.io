import requests
import json
import mysql.connector

# Configura la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="Meassures"
)

# Crea la tabla de datos
cursor = db.cursor()
cursor.execute("""
CREATE TABLE data (
  id INT NOT NULL AUTO_INCREMENT,
  device_id VARCHAR(255) NOT NULL,
  measurement1 VARCHAR(255) NOT NULL,
  measurement2 VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);
""")

# Escucha las solicitudes POST
def handle_post(req):
    # Obtén los datos de la solicitud
    data = json.loads(req.data)

    # Almacena los datos en la base de datos
    cursor.execute("""
    INSERT INTO data (
      device_id,
      measurement1,
      measurement2,
      created_at
    ) VALUES (
      %s,
      %s,
      %s,
      %s
    );
    """, (
        data["device_id"],
        data["measurement1"],
        data["measurement2"],
        data["created_at"]
    ))
    db.commit()

    return "OK"

# Inicia el servidor
app = Flask(__name__)
app.route("/", methods=["POST"])(handle_post)
app.run(debug=True)