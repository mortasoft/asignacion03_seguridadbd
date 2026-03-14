import pyodbc
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Configuracion de conexion al contenedor 'db'
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=db;"
    "DATABASE=master;"
    "UID=sa;"
    "PWD=Seguridad_2026!;"
    "TrustServerCertificate=yes;"
)

@app.route('/cliente')
def buscar():
    apellido = request.args.get('apellido')

    # Manejo basico si no envian parametro
    if not apellido:
        return "Por favor usa el parametro ?apellido=", 400

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # --- AQUI ESTA EL PROBLEMA: SQL INJECTION ---
        # El valor de 'apellido' se concatena directo al string SQL sin ninguna proteccion.
        # Esto permite que un atacante inyecte codigo SQL arbitrario.
        query = "SELECT name, database_id FROM sys.databases WHERE name LIKE '" + apellido + "'"

        cursor.execute(query)
        rows = cursor.fetchall()

        resultados = [{"nombre_db": r[0], "id": r[1]} for r in rows]
        # Incluimos la query ejecutada para fines educativos
        return jsonify({"query_ejecutada": query, "resultados": resultados})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # host 0.0.0.0 para que sea accesible desde fuera del contenedor
    app.run(host='0.0.0.0', port=5000)
