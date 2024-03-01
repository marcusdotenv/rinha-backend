from fastapi import HTTPException

def get_current_accumulated_balance(client_id, cursor):
    query_current_balance = """SELECT SUM(
                CASE
                    WHEN tipo = 'd' THEN -valor
                    WHEN tipo = 'c' THEN valor
                END
            ) as valor_acumulado 
            FROM transacoes WHERE cliente_id=%(id)s"""
    cursor.execute(query_current_balance, {"id": client_id})
    accumulated_transactions = cursor.fetchall()
    final_value = accumulated_transactions[0].get("valor_acumulado", 0)

    return 0 if final_value == None else final_value
    
def get_client_data(client_id, cursor):
    query_user_data = """ SELECT saldo_inicial, limite FROM clientes WHERE id=%(id)s"""
    cursor.execute(query_user_data, {"id": client_id})
    registered_client = cursor.fetchall() 

    if len(registered_client) == 0: raise HTTPException(status_code=404, detail=f"Client not found")

    return registered_client[0]

def get_client_last_transactions(cliente_id, limit, cursor):
    query_current_balance = """
        SELECT valor, tipo, descricao, realizada_em FROM transacoes
        WHERE cliente_id=%(id)s
        ORDER BY realizada_em DESC
        LIMIT %(limit)s
    """
    cursor.execute(query_current_balance, {"id": cliente_id, "limit": limit})
    last_transactions = cursor.fetchall()

    return last_transactions

def save_transaction(new_transaction, cursor):
    querySaveNewTransaction = """
        INSERT INTO transacoes (valor, tipo, descricao, cliente_id)
        VALUES (%(valor)s, %(tipo)s, %(descricao)s, %(cliente_id)s)
    """
    cursor.execute(querySaveNewTransaction, new_transaction)


def validate_new_transaction(new_transaction):
    expected_keys = ["tipo", "valor", "descricao"]
    for key in expected_keys:
        if key not in new_transaction: raise HTTPException(status_code=400, detail=f"{key} is necessary")

    if len(new_transaction["descricao"]) > 10: 
        raise HTTPException(status_code=400, detail="invalid description")

    if len(new_transaction["tipo"]) > 1 or ( new_transaction["tipo"] != "d" and new_transaction["tipo"] != "c"): 
        raise HTTPException(status_code=400, detail="invalid type")

    if new_transaction["valor"] < 0 or new_transaction["valor"] != int(new_transaction["valor"]):
        raise HTTPException(status_code=400, detail="invalid value")