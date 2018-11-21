# In[]
# Importing the necessary libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

# In[]
# Web scrapping
url = 'https://www.passportindex.org/byHistoric.php'

response=requests.get(url)
page_content = BeautifulSoup(response.text, "html.parser")

country_names = []
rank_2018 = []; score_2018 = []
rank_2017 = []; score_2017 = []
rank_2016 = []; score_2016 = []
rank_2015 = []; score_2015 = []

for tr in page_content.find_all('tr')[2:][:-4]:
    tds = tr.find_all('td')
    
    country_names.append(tds[0].text)
    score_2018.append(int(tds[1].text.split(' ')[1]))
    rank_2018.append(int(tds[1].text.split(' ')[4]))
    
    score_2017.append(int(tds[2].text.split(' ')[1]))
    rank_2017.append(int(tds[2].text.split(' ')[4]))
    
    score_2016.append(int(tds[3].text.split(' ')[1]))
    rank_2016.append(int(tds[3].text.split(' ')[4]))
    
    score_2015.append(int(tds[4].text.split(' ')[0]))
    rank_2015.append(int(tds[4].text.split(' ')[2]))
    
table = [rank_2018, score_2018, rank_2017, score_2017, rank_2016, score_2016, rank_2015, score_2015]
table = np.array(table)
table = np.transpose(table)

Table = pd.DataFrame(table, columns= ['rank_2018','visa_free_score_2018','rank_2017','visa_free_score_2017','rank_2016','visa_free_score_2016','rank_2015','visa_free_score_2015'])
Table['Country_name'] = country_names

Table.to_csv('Passport_index.csv', index =False)

# In[]
# Tracking the relative change of Global passport index ranking
Table['change_index'] = Table.rank_2015 - Table.rank_2018
Table = Table.sort_values('change_index')

plt.figure(figsize=(20,10))
f = sns.barplot(Table['Country_name'], Table['change_index'])
f.set_xticklabels(f.get_xticklabels(), rotation=90, fontsize=8)

# In[]
# Tracking the relative change of visa free score
Table['change_index'] = Table.visa_free_score_2018 - Table.visa_free_score_2015
Table = Table.sort_values('change_index')

plt.figure(figsize=(20,10))
f = sns.barplot(Table['Country_name'], Table['change_index'])
f.set_xticklabels(f.get_xticklabels(), rotation=90, fontsize=8)

# In[]
# Change in visa score with economic state
# Mention preprocessing

Table = Table.sort_values('rank_2018')
eco_status = pd.read_csv(r"C:\Users\srinesh\Documents\Projects\Personal_learning\Passport Index\Country_status.csv", encoding='latin-1')
merge_data = Table.merge(eco_status, how = 'inner', left_on='Country_name', right_on='TableName')

plt.figure(figsize=(20,10))
f = sns.barplot(merge_data['IncomeGroup'],merge_data['rank_2018'])
f.set_xticklabels(f.get_xticklabels(), rotation=0, fontsize=8)

# In[]
# 
migrant_population = pd.read_csv(r"C:\Users\srinesh\Documents\Projects\Personal_learning\Passport Index\migrant_population.csv", encoding='latin-1')
migrant_population = migrant_population[['Country Code', 'Country Name', '2010','2011','2012','2013','2014','2015','2016']]
migrant_population['average_pop'] = migrant_population.mean(axis=1)
migrant_population = migrant_population[['Country Code', 'Country Name', 'average_pop']]
merge_data2 = merge_data.merge(migrant_population, how = 'inner', on='Country Code').sort_values('average_pop')

ax = sns.lmplot('rank_2018', 'average_pop', hue="IncomeGroup", data= merge_data2)
ax.set(yscale="log")
