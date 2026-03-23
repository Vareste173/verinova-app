#mysql ile bağlantı
from sqlalchemy import create_engine, text
import pandas 

#baglantı adresi alır
def get_engine(connection_string):
    return create_engine(connection_string)

#pandas dataFrameyi veri tabanına kaydeder
def save_dataframe(df: pandas.DataFrame, table_name: str, connection_string: str):
    engine = get_engine(connection_string)
    #asagı satırda tablo varsa sonuna ekle veriyi silme ve indexi kaydetme
    with engine.begin() as conn:
        df.to_sql(table_name, con=conn, if_exists="append", index=False)

#DataFrame'i tabloya kaydeder ve eklenen satırın ID'sini döndürür.
def save_and_return_id(df: pandas.DataFrame, table_name: str, connection_string: str, id_column: str):
    engine = get_engine(connection_string)
    #eklenen son satırın ID numarasını alır.
    with engine.begin() as conn:
        df.to_sql(table_name, con=conn, if_exists="append", index=False)
        result = conn.execute(text("SELECT LAST_INSERT_ID()")).scalar()
    return result
