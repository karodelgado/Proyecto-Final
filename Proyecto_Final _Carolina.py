# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 14:30:23 2024

@author: Estudiante
"""

import pandas as pd
import sqlite3
from flask import Flask, jsonify
import os
import sys

app = Flask(__name__)

def inicializar_bd():
    """
    Inicializa la base de datos leyendo un archivo CSV y creando una tabla SQL.
    """
    try:
        directorio_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
        os.chdir(directorio_actual)  # Cambia solo al directorio, no al archivo
        
        # Lee el archivo CSV
        df = pd.read_csv('hockey_teams_data.csv')
        # Conecta a la base de datos SQLite
        conn = sqlite3.connect('hockey_teams.db')
        # Crea la tabla 'pedidos' a partir del DataFrame
        df.to_sql('teams', conn, if_exists='replace', index=False)
        conn.close()
        print("Base de datos inicializada exitosamente")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")

# Inicializa la base de datos al inicio
inicializar_bd()

def obtener_conexion_bd():
    """
    Establece y retorna una conexión a la base de datos.
    """
    return sqlite3.connect('hockey_teams.db')

@app.route('/teams/<team_name>', methods=['GET'])
def obtener_equipo(team_name):
    """
    Maneja la solicitud GET para obtener un pedido específico.
    """
    conn = obtener_conexion_bd()
    try:
        # Ejecuta la consulta SQL para obtener el pedido
        resultado = conn.execute("SELECT * FROM teams WHERE team_name = ?", (team_name,)).fetchone()
        if resultado:
            # Obtiene los nombres de las columnas
            columnas = [description[0] for description in conn.execute("SELECT * FROM teams LIMIT 1").description]
            # Convierte el resultado a un diccionario
            pedido = dict(zip(columnas, resultado))
            return jsonify(pedido)
        else:
            return jsonify({"error": "Pedido no encontrado"}), 404
    finally:
        conn.close()

if __name__ == '__main__':
    # Inicia la aplicación Flask
    app.run(debug=False, port=5000)
    
    
    