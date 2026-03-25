from fastapi import APIRouter
import sys
import os
# Üst klasörlere yol ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from blockchain.blockchain import Blockchain
import pandas
from src.database.db_connection import save_dataframe

router = APIRouter()
blockchain = Blockchain()
connection_string = "mysql+pymysql://root:1234@localhost:3306/fintech_db"
@router.post("/blockchain/transaction")
def add_transaction(data: dict):
    # Blockchain'e ekle
    blockchain.add_transaction(data)

    # SQL'e logla
    df = pandas.DataFrame([{
        "meta_key": "transaction",
        "meta_value": str(data)
    }])
    save_dataframe(df, "transactions_metadata", connection_string)

    return {"status": "ok", "chain_length": len(blockchain.chain)}

@router.get("/blockchain/chain")
def get_chain():
    return {"chain": blockchain.chain}

@router.get("/validate")
def is_blockchain_valid():
    is_valid = blockchain.is_chain_valid()
    return {"is_valid": is_valid}
