import csv
import urllib
import pandas as pd
from dateutil.parser import parse
from sqlalchemy import Column, Date, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from devices_thread import get_devices


params = urllib.parse.quote_plus(
    r"Driver={ODBC Driver 18 for SQL Server};Server=tcp:server-name.database.windows.net,1433;Database=maas_360;Uid=user;Pwd=password!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)
conn_str = "mssql+pyodbc:///?odbc_connect={}".format(params)
engine_azure = create_engine(conn_str, echo=True)


print("connection is ok")

devices = get_devices()

data = pd.DataFrame(devices)
data.to_sql("devices", engine_azure)
