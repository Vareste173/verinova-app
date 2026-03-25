from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from blockchain import Blockchain

app = FastAPI()

db_config = {
  "host": "localhost",
  "user": "root",
  "password": "12345",
  "database": "kutuphane_db"
}

class BlockData(BaseModel):
  data:str

blockchain_= Blockchain()

def get_valid_blockchain():
  if not blockchain_.is_chain_valid():
    raise HTTPException(status_code=400, detail="The chain is invalid")
  return blockchain_


@app.post("/mine_block/")
def mine_block(block_data: BlockData,
               blockchain: Blockchain = Depends(get_valid_blockchain)):
  new_block = blockchain.add_block(new_data=block_data.data)
  return new_block.__dict__


@app.get("/get_blockchain/")
def get_blockchain(blockchain: Blockchain = Depends(get_valid_blockchain)):
  chain_data = [block.__dict__ for block in blockchain.chain]
  return {"lenght": len(blockchain.chain), "chain": chain_data}

@app.get("/blockchain/last/")
def get_previous_block(blockchain: Blockchain= Depends(get_valid_blockchain)):
  return blockchain.get_previous_block()

@app.get("/validate")
def is_block_valid():
  is_valid = blockchain_.is_chain_valid()
  return {"is_valid": is_valid}