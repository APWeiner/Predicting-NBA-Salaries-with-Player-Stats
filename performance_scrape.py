#Make necessary imports
import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import unicodedata

#Specifying year to retrieve data for (year = 2024 => 2023-24 season)
year = 2024


####Salary Data Scraping####
#Creating dataframe to store player |salary data
salary_df = pd.DataFrame()

#Creating a string based on specified year to extract data from url
year_string = str(year-1)+"-"+str(year)

##Only use this if not working with current NBA season!
#url = "https://hoopshype.com/salaries/players/"+year_string+"/"

#URL of hoopshype player salary data for current season
url = "https://hoopshype.com/salaries/players/"

#Sending a GET request to the URL and saving as response
response = requests.get(url)

#Creating dataframe to store player salary data
salary_df = pd.DataFrame(columns=['Player',"Salary"])

#Using BeautifulSoup's HTML parser
soup = BS(response.content, 'html.parser')
#Finding the table
table = soup.find('table')
if not table:
    print("bad")
if table:
    print("Table Found!")
    #Finding the table body
    tbody = soup.find('tbody')
    if tbody:
        print("Tbody found!")
                
        #Finding rows containing each player
        rows = tbody.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            #Cleaning cells from uneccesary escape sequences and characters
            cleaned_cells = [cell.text.replace('\n', '').replace('\t', '').replace('$', '').replace(',','') for cell in cells]
            #Putting Player and salary at end of the salary_df
            salary_df.loc[len(salary_df)]=cleaned_cells[1:3]



####Per-Game Stats Scraping####
#URL of scraped website, Basketball Reference's per game stats for players
url = "https://www.basketball-reference.com/leagues/NBA_"+str(year)+"_per_game.html"

#Sending a GET request to the URL and saving as response
response = requests.get(url)

#Parsing the HTML content of the response using BeautifulSoup
soup = BS(response.content, 'html.parser')

#Finding the table element of the webpage
table = soup.find('table')
if table:
    print("Table Found!")
#Finding the table head which contains the names of stats
thead = table.find('thead')
if thead:
    print('Thead Found!')
#Finding the row in the table head
header_row = thead.find('tr')
if header_row:
    print('Header Row Found!')
#Creating a list of the names of the different stats from the cells in the header row
col_list = []
cols = header_row.find_all('th')
for col in cols:
    col_list.append(col.text)
col_list = col_list[1:]

#Creating dataframe to store per game data with stats as columns
per_game_df = pd.DataFrame(columns=col_list)

#Finding the body of the table with actual stats
tbody = table.find('tbody')  
if tbody:
    print('tbody found!') 
#Rows of stats corresponding to players
rows = tbody.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    for cell in cells:
        #Removing uneccesary characters and escape sequences from datacells
        cleaned_cells = [cell.text.replace('\n', '').replace('\t', '').replace('$', '').replace(',','') for cell in cells]
    #Adding the cleaned cells to the end of the dataframe
    per_game_df.loc[len(per_game_df)]=cleaned_cells

#Function for normalizing characters i.e Luka Dončić => Luka Doncic
def normalize_characters(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
per_game_df['Player'] = per_game_df['Player'].apply(normalize_characters)

####Scraping for Advanced Stats####
#Methods are generally same as per-game scraping
url = "https://www.basketball-reference.com/leagues/NBA_"+str(year)+"_advanced.html"
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

advanced_df = pd.DataFrame(columns=col_list)
tbody = table.find('tbody')  
if tbody:
    print('tbody found!') 
rows = tbody.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    for cell in cells:
        cleaned_cells = [cell.text.replace('\n', '').replace('\t', '').replace('$', '').replace(',','') for cell in cells]
    advanced_df.loc[len(advanced_df)]=cleaned_cells

advanced_df['Player'] = advanced_df['Player'].apply(normalize_characters)

####Remove duplicate columns from advanced_df besides 'Player'####
per_game_columns = per_game_df.columns.drop('Player')
advanced_columns = advanced_df.columns
common_stats = set(per_game_columns).intersection(set(advanced_columns))
advanced_columns = [stat for stat in advanced_columns if stat not in common_stats]
advanced_df = advanced_df.loc[:, advanced_columns]

####Players who were traded have multiple entries. Their first occurence is total season####
per_game_df.drop_duplicates(subset='Player',keep='first',inplace=True)
advanced_df.drop_duplicates(subset='Player',keep='first',inplace=True)


####Merging all dataframes on 'Player' column and exporting to 'current stats and salaries.csv'####
final_df = pd.merge(per_game_df, advanced_df, on='Player')
final_df = pd.merge(salary_df, final_df, on='Player')
final_df.to_csv('current stats and salaries.csv', index=False)
