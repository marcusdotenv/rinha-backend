import datetime
from uuid import UUID
from utils import *
from fastapi import FastAPI, HTTPException
from db import connect_db
from psycopg2.extras import RealDictCursor
import uuid


app = FastAPI()
instance_id = uuid.uuid4()

@app.get("/")
def check():
    return {"instance": instance_id}


@app.post("/clientes/{cliente_id}/transacoes")
def nova_transacao(new_transaction: dict, cliente_id: int):

    validate_new_transaction(new_transaction)
    db = connect_db()
    try:
        with db.cursor(cursor_factory=RealDictCursor) as cursor:
            db.autocommit = False

            client_data = get_client_data(cliente_id, cursor)
            accumulated_transaction_balance = get_current_accumulated_balance(cliente_id, cursor)
            new_transaction_value = new_transaction["valor"]*-1 if new_transaction["tipo"] == "d" else new_transaction["valor"]

            balance_after_transaction_saved = new_transaction_value + accumulated_transaction_balance + client_data["saldo_inicial"]
            if balance_after_transaction_saved < -client_data["limite"]: raise HTTPException(status_code=422, detail=f"invalid transaction")

            save_transaction({**new_transaction, "cliente_id":cliente_id}, cursor)
            db.commit()

            return {
                "limite": client_data["limite"],
                "saldo": balance_after_transaction_saved
            }

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@app.get("/clientes/{cliente_id}/extrato")
def extrato(cliente_id: int):
    db = connect_db()
    cursor = db.cursor(cursor_factory=RealDictCursor)

    client_data = get_client_data(cliente_id, cursor)

    accumulated_transaction_balance = get_current_accumulated_balance(cliente_id, cursor)

    last_transactions = get_client_last_transactions(cliente_id, 10, cursor)

    db.close()

    return {
        "saldo": {
            "total": accumulated_transaction_balance+client_data["saldo_inicial"],
            "data_extrato": datetime.datetime.now(),
            "limite": client_data["limite"]
        },
        "ultimas_transacoes": last_transactions
    }