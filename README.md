# Predicting-NBA-Salaries-with-Player-Stats
Linear regression model that estimates an NBA player's salary based on certain stats using training data from the 2022-2023 season.
The process, results, and analysis of the model were reported for Bruin Sports Analytic's data journalism in this article here: https://www.bruinsportsanalytics.com/post/nba-ballers .



The model was reused to estimate player's salaries for the current 2023-2024 season as of 2/8/2024:
The Players with the Top 10 Highest Estimated Salaries so Far:
1. Nikola Jokic
2. Luka Doncic
3. Giannis Antetokounmpo
4. Joel Embiid
5. Shai Gilgeous-Alexander

The Current Top 5 on the KIA Race to MVP Ladder:
1. Nikola Jokic
2. Shai Gilgeous-Alexander
3. Joel Embiid
4. Giannis Antetokounmpo
5. Jayson Tatum

4 out of 5 of the names are present on both lists. However, Luka Doncic who the model ranked 2nd is 6th on the KIA MVP Ladder.

The two powerhouse rookies battling out for rookie of the year are Victor Wembanyama and Chet Holmgren.
As of writing, both the Rookie of the Year Ladder and the model edge Victor over Chet.

The model is trained on the target variable, salaries granted to NBA players by franchises, which is not necessarily wholly representative of a player's on-court contributions. However, the better a player is, the  better they tend to earn, so the salary estimations are indiscriminately used as metrics of a player's value here.



-performance_scrape.py: Scraped NBA player stats and salaries from Basketball Reference and HoopsHype using BeautfulSoup's HTML parser. The same code with some adjustments was used to create both csv files.

-Model Training.ipynb: Documents how the model was trained including feature selection and performance evaluation

-Current Season.ipynb: Uses the previously trained model to estimate a player's salary based on their current 2023-24 season performance

