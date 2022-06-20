"""!
@mainpage Scraping de Rastreamento de Correios
Trabalho para P2 do curso de Engenharia de Software
@section Disciplina
Laborátorio de Programação com Interface com o Usuário
@section Professor
André Saraiva
@section Aluno
Almir de Souza Pontes Junior - Mat: 202021932
@author Pontes Junior
@version 1.0 - python 3.10 - Flask 2.1.2
@date 05/06/2022
@copyright GNU Public Licence
"""

import sqlite3

def conectar():
    return sqlite3.connect("rastreio.db")

def monta_tabelas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS rastreio(codigo TEXT, numero TEXT, status TEXT)")
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(e)
    finally:
        conn.close()

def insere_rastreio(codigo, numero, status):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rastreio VALUES('"+codigo+"','"+numero+"','"+status+"')")
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(e)
    finally:
        conn.close()       

def remove_rastreio(code):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rastreio WHERE codigo = '"+code+"'")
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(e)
    finally:
        conn.close()

def select_rastreio():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rastreio")
        dados = cursor.fetchall()
        return dados
    except sqlite3.DatabaseError as e:
        print(e)
    finally:
        conn.close()

def select_codigo_rastreio(code):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT codigo FROM rastreio WHERE codigo='"+code+"'")
        return cursor.fetchone()
        
    except sqlite3.DatabaseError as e:
        print(e)
    finally:
        conn.close()

