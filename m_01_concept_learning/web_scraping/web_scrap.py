# Scenario

# Consider that you have been hired by a Multiplex management organization to extract the information of the top 50 movies with the best average rating from the web link shared below.

# https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films

# The information required is Average Rank, Film, and Year.
# You are required to write a Python script webscraping_movies.py that extracts the information and saves it to a CSV file top_50_films.csv. You are also required to save the same information to a database Movies.db under the table name Top_50.

# Required Libs
import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3
# Constants

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'

db_name = "Movies.db"
table_name = "Top_50"

csv_path = "top_50_films.csv"
df =  pd.DataFrame(columns=["Average Rank","Film","Year"])
count = 0

# Get Html Data

html_page = requests.get(url).text
data = BeautifulSoup(html_page, "html.parser")

tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

for row in rows:
    if count<=50:
        column = row.find_all('td')
        if len(column)!=0:
            data_dict = {
                # contents gives a list even if there only one element in it
                "Average Rank": int(column[0].contents[0]), 
                "Film": column[1].contents[0],
                "Year": int(column[2].contents[0])

            }
            df_instant = pd.DataFrame(data_dict, index= [0])
            
            # main dataframe concatination
            df = pd.concat([df,df_instant], ignore_index=True)

            count += 1
    else:
        break

# Storing data in sqlite db

df.to_csv(csv_path)
conn = sqlite3.connect(db_name)
df.to_sql(table_name,conn, if_exists= 'replace', index=False)
conn.close()
