#Frontent ile baglantı
from fastapi import FastAPI, UploadFile, Form
from src.reader.file_reader import process_file
from src.preprocessing.text_cleaner import clean_dataframe
from src.database.db_connection import save_dataframe
import pandas
from src.services import blockchain_service

app = FastAPI()
connection_string = "mysql+pymysql://root:1234@localhost:3306/fintech_db"

@app.post("/login")
def login(email: str = Form(...), phone: str = Form(...)):
    import mysql.connector
    conn = mysql.connector.connect(
        host="localhost", user="root", password="1234", database="fintech_db"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users_core WHERE email=%s AND phone=%s", (email, phone))
    result = cursor.fetchone()
    if result:
        return {"status": "success", "user": result}
    return {"status": "error", "message": "Invalid credentials"}

@app.post("/upload")
async def upload_file(file: UploadFile, user_id: int = Form(...)):
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    process_file(file_path, connection_string, user_id)
    return {"status": "ok", "message": "File processed"}


app.include_router(blockchain_service.router)
