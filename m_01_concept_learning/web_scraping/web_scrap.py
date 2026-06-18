# https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films

# The information required is Rotton Tommato Rank, Film, and Year. of 2000s "2000" included, and only top 25

# Required Libs
import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3
# Constants

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'

db_name = "Movies.db"
table_name = "Rotton_25"

csv_path = "top_25_rotton_films.csv"
df =  pd.DataFrame(columns=["Rotton Tommato","Film","Year"])
count = 0

# Get Html Data

html_page = requests.get(url).text
data = BeautifulSoup(html_page, "html.parser")

tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

for row in rows:
        column = row.find_all('td')
        if len(column)!=0:
            if column[2].contents[0] != 'unranked' and column[3].contents[0] != 'unranked' :
                if int(column[2].contents[0]) <= 2000: 
                    data_dict = {
                        # contents gives a list even if there only one element in it
                        "Rotton Tommato": int(column[3].contents[0]), 
                        "Film": column[1].contents[0],
                        "Year": int(column[2].contents[0])
                    }
                    df_instant = pd.DataFrame(data_dict, index= [0])
                    # main dataframe concatination
                    df = pd.concat([df,df_instant], ignore_index=True)

                    count += 1
                else:
                    pass
            else:
                pass

# Top 25 movies of 2000s from available Rotton Tommato Rank on the webpage , unranked are not included

df = df.sort_values(by="Rotton Tommato",ignore_index=True)[:25]
print(df)
# Storing data in sqlite db

df.to_csv(csv_path)
conn = sqlite3.connect(db_name)
df.to_sql(table_name,conn, if_exists= 'replace', index=False)
conn.close()
