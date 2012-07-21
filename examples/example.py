import os
import sqlite3
from gviz_data_table import data_table

folder = os.path.split(__file__)[0]
db = sqlite3.connect(os.path.join(folder, "sample.db"))
c = db.cursor()
c.execute("SELECT * FROM employees")
cols = [col[0] for col in c.description]
