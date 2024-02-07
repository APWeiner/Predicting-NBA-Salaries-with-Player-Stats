import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import unicodedata

#salaries webpage URL

#get headers
url = "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"
response = requests.get(url)
soup = BS(response.content, 'html.parser')
table = soup.find('table')
if table:
    print("Table Found!")
thead = table.find('thead')
if thead:
    print('Thead Found!')
header_row = thead.find('tr')
if header_row:
    print('Header Row Found!')
col_list = []
cols = header_row.find_all('th')
for col in cols:
    col_list.append(col.text)
col_list = col_list[1:]

first = True
year = 2024
final_df = pd.DataFrame(columns=col_list)
tbody = table.find('tbody')  
if tbody:
    print('tbody found!') 
rows = tbody.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    for cell in cells:
        cleaned_cells = [cell.text.replace('\n', '').replace('\t', '').replace('$', '').replace(',','') for cell in cells]
    final_df.loc[len(final_df)]=cleaned_cells

salary_df = pd.read_csv('salaries_with_24.csv')

salary24df = salary_df[['Player','2023-2024']]

def normalize_characters(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
final_df['Player'] = final_df['Player'].apply(normalize_characters)

salaries_merged_df = pd.merge(salary24df, final_df, on='Player', how='outer')

url = "https://www.basketball-reference.com/leagues/NBA_2024_advanced.html"
response = requests.get(url)
soup = BS(response.content, 'html.parser')
table = soup.find('table')
if table:
    print("Table Found!")
thead = table.find('thead')
if thead:
    print('Thead Found!')
header_row = thead.find('tr')
if header_row:
    print('Header Row Found!')
col_list = []
cols = header_row.find_all('th')
for col in cols:
    col_list.append(col.text)
col_list = col_list[1:]

first = True
year = 2024
final_df = pd.DataFrame(columns=col_list)
tbody = table.find('tbody')  
if tbody:
    print('tbody found!') 
rows = tbody.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    for cell in cells:
        cleaned_cells = [cell.text.replace('\n', '').replace('\t', '').replace('$', '').replace(',','') for cell in cells]
    final_df.loc[len(final_df)]=cleaned_cells

def normalize_characters(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
final_df['Player'] = final_df['Player'].apply(normalize_characters)

salaries_merged_df = pd.merge(salaries_merged_df, final_df, on='Player', how='outer')

salaries_merged_df.dropna(subset=['2023-2024'], inplace=True)

salaries_merged_df.to_csv('current salaries and performances.csv', index=False)


