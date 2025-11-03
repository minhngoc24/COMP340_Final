import psycopg
from psycopg.rows import dict_row
from dbinfo import *

conn = psycopg.connect(
    f"host=localhost dbname=gymfinder user={DBUSER} password={DBPASS}"
)

print("✅ Connection successful!")
print(f"Database: {conn.info.dbname}")
print(f"User: {conn.info.user}")
print(f"Host: {conn.info.host}")
print(f"Port: {conn.info.port}")
print(f"Backend PID: {conn.info.backend_pid}")
print(f"Server version: {conn.info.server_version}")
print(f"Client encoding: {conn.info.encoding}")

conn.close()
