import pandas as pd
import sqlite3

db_name = "STAFF.db"
table_name = "INSTRUCTOR"


attribute_list = ["ID","FNAME","LNAME","CITY","CCODE"]

file_path = "./INSTRUCTOR.csv"

df = pd.read_csv(file_path, names = attribute_list)

conn = sqlite3.connect(db_name)

df.to_sql(table_name,conn, if_exists= "replace", index=False)

print("table is created")


data_dict = {'ID' : [100],
            'FNAME' : ['John'],
            'LNAME' : ['Doe'],
            'CITY' : ['Paris'],
            'CCODE' : ['FR']}

data_append = pd.DataFrame(data_dict)

data_append.to_sql(table_name,conn, if_exists= "append", index=False)

query_statement = f"SELECT * FROM {table_name} WHERE CCODE = 'FR' "

query_output = pd.read_sql(query_statement, conn)

print(query_output)

conn.close()