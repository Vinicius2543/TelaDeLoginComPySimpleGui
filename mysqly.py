import mysql.connector as mysql

def cria_banco_tabela():
    ok = False
    ativa = False
    while ok == False:
        banco = mysql.connect(
            host="localhost",
            user="root",
            password=""
            )
        if ativa == True:
            banco = mysql.connect(
                host="localhost",
                database='cadastro',
                user="root",
                password=""
            )
        cursor = banco.cursor()
        try:
            cursor.execute("CREATE DATABASE cadastro")
            ativa = True
        except:
            cursor.execute("CREATE TABLE pessoas(nome varchar(70),usuario varchar(14),senha varchar(20))")
            ok = True
    return 'Base de dados criada'


def valores_database():
    global banco
    try:
        banco = mysql.connect(
        host="localhost",
        database='cadastro',
        user="root",
        password=""
        )

    except mysql.Error as erro:
        print(f'ERRO:{erro}')

    return banco


