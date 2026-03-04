import pyodbc
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración de conexión al contenedor 'db'
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
    
    # Manejo básico si no envían parámetro
    if not apellido:
        return "Por favor usa el parámetro ?apellido=", 400

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # --- AQUÍ ESTÁ EL PROBLEMA: SQL INJECTION ---
        # El valor de 'apellido' se mete directo al string sin protección
        query = f"SELECT name, database_id FROM sys.databases WHERE name LIKE '{apellido}%'"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Convertir resultados a JSON
        resultados = [{"nombre_db": r[0], "id": r[1]} for r in rows]
        return jsonify(resultados)
        
    except Exception as e:
        return f"Error de conexión: {str(e)}", 500

if __name__ == '__main__':
    # Importante: host 0.0.0.0 para que sea accesible desde afuera del contenedor
    app.run(host='0.0.0.0', port=5000)
