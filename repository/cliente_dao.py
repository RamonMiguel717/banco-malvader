from repository.conexao import obter_conexao

def buscar_todos_clientes():
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente")
    resultado = cursor.fetchall()
    conn.close()
    return resultado
