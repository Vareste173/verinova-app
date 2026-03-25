from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.src.dependencies import get_db


# Router tanımı
blockchain_service = APIRouter()

# Örnek endpoint: blockchain durumu
@blockchain_service.get("/api/blockchain/status")
def get_status(db: Session = Depends(get_db)):
    return {"status": "Blockchain servisi aktif"}

# Örnek endpoint: wallet bilgisi
@blockchain_service.get("/api/blockchain/wallet")
def get_wallet(db: Session = Depends(get_db)):
    # Burada DB veya blockchain logic eklenebilir
    return {"wallet": "0x123456789abcdef"}
