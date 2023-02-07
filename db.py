import csv
import urllib
import pandas as pd
from dateutil.parser import parse
from sqlalchemy import Column, Date, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from devices_thread import get_devices


def create_db_engine_object():
    try:
        load_dotenv()
        DB_SERVER = os.environ.get("DB_SERVER")
        DATABASE = os.environ.get("DATABASE")
        DB_USER = os.environ.get("DB_USER")
        DB_PSWD = os.environ.get("DB_PSWD")
        params = urllib.parse.quote_plus(
            rf"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{DB_SERVER}.database.windows.net,1433;Database={DATABASE};Uid={DB_USER};Pwd={DB_PSWD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        )
        conn_str = "mssql+pyodbc:///?odbc_connect={}".format(params)
        engine = create_engine(conn_str, echo=True)
        return engine
    except Exception as e:
        print(f"Erro ao criar o objeto de engine: {e}")
        return None


def dataframe_to_db(db_engine=create_db_engine_object()):
    devices = get_devices()
    data = pd.DataFrame(devices)

    data["lastReported"] = pd.to_datetime(data["lastReported"])
    data["lastReported"] = data["lastReported"].dt.strftime("%d/%m/%Y")
    data.to_sql("devices", db_engine, if_exists="replace")


if __name__ == "__main__":
    dataframe_to_db()
