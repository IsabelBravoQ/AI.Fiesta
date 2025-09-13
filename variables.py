import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

config = {
    "host":os.environ.get("HOST_AWS"),
    "user":"postgres",
    "password":os.environ.get("PASSWORD_AWS"),
    "port": 5432,
    "dbname": "postgres"
}