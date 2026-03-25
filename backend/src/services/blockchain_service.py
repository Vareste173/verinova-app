from fastapi import APIRouter
import sys, os
import pandas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from blockchain.blockchain import Blockchain
from backend.src.database.db_connection import save_dataframe

# Router ve blockchain objesi
router = APIRouter()
blockchain = Blockchain()

# MySQL bağlantı stringi
connection_string = "mysql+pymysql://root:1234@localhost:3306/fintech_db"

# SQLAlchemy engine ve session
engine = create_engine(connection_string)
SessionLocal = sessionmaker(bind=engine)

@router.post("/blockchain/transaction")
def add_transaction(data: dict):
    # 1. Blockchain'e ekle
    blockchain.add_transaction(data)

    # 2. SQL'e logla
    db = SessionLocal()
    try:
        # Önce transactions_core tablosuna kayıt ekle
        core_df = pandas.DataFrame([{
            "user_id": 1,  # test için sabit, ileride request’ten gelecek
            "file_name": "blockchain_tx",
            "file_type": "json"
        }])
        save_dataframe(core_df, "transactions_core", connection_string)

        # Son eklenen transaction_id’yi al
        last_id = db.execute("SELECT LAST_INSERT_ID()").scalar()

        # Metadata tablosuna kayıt ekle
        meta_df = pandas.DataFrame([{
            "transaction_id": last_id,
            "meta_key": "transaction",
            "meta_value": str(data)
        }])
        save_dataframe(meta_df, "transactions_metadata", connection_string)

        return {
            "status": "ok",
            "chain_length": len(blockchain.chain),
            "transaction_id": last_id
        }
    finally:
        db.close()

@router.get("/blockchain/chain")
def get_chain():
    return {"chain": blockchain.chain}

@router.get("/validate")
def is_blockchain_valid():
    is_valid = blockchain.is_chain_valid()
    return {"is_valid": is_valid}
