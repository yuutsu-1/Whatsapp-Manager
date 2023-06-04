import pyodbc
import os
import json

connStr = (
    r'DSN=whatsmanager;'
    r'Database=WhatsappSender-DEV;'
    r'Trusted_Connection=yes;'
    )

cnxn = pyodbc.connect(connStr)

cursor = cnxn.cursor()
cursor.execute("INSERT INTO CLIENTES (id, nome, sobrenome, telefone, data_nascimento, ativo) VALUES (3, 'Erika', 'Pinheiro', '63984208152', '15/10/2002', 'S')") 
cursor.execute('commit')

cursor.execute("SELECT * FROM CLIENTES") 
row = cursor.fetchone() 
while row:
    print (row) 
    row = cursor.fetchone()