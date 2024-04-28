import sqlite3 
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(f"{path}/var/database.sqlite")
cur = conn.cursor()

