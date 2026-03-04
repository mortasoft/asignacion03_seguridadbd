import pyodbc
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración de conexión (usamos el mismo nombre de servicio 'db')
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
    if not apellido:
        return "Por favor usa el parámetro ?apellido=", 400

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # --- VERSIÓN SEGURA: CONSULTA PARAMETRIZADA ---
        # El '?' actúa como un marcador de posición. El driver limpia los datos.
        query = "SELECT name, database_id FROM sys.databases WHERE name LIKE ?"
        
        # Los datos se pasan como una tupla separada de la lógica SQL
        cursor.execute(query, (f"{apellido}%",))
        
        rows = cursor.fetchall()
        resultados = [{"nombre_db": r[0], "id": r[1]} for r in rows]
        return jsonify(resultados)
        
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
