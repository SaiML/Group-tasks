import ast
import pandas as pd
from datetime import datetime as dt
pd.set_option('Display.max_columns', 100)
import matplotlib.pyplot as plt
ted_talks_df = pd.read_csv('ted_main.csv')

# Q-1-a
# Top 5 talks according to comments
print(ted_talks_df.sort_values('comments', ascending=False)[['title', 'main_speaker']][:5])



# Q-1-b
# Hist plots for comments<1000 and comments>1000
plt.figure(figsize=(10,8))
plt.hist(ted_talks_df[ted_talks_df['comments']<1000]['comments'], bins=20)
plt.hist(ted_talks_df[ted_talks_df['comments']>=1000]['comments'], bins=50, color='r')
plt.show()
print('''it can be seen that there are quite a few outliers, 3 above the value of 3000. They are spread 
far away from the body of the distribution''')


# Q-1-c
# No of talks happening each year and the distribution
ted_talks_df['year'] = pd.to_datetime(ted_talks_df['film_date'], unit='s').dt.year
by_year = ted_talks_df.groupby('year').count()
plt.bar(by_year.index, by_year['title'])
plt.show()



# Average delay between filming and publishing
ted_talks_df['film_date'] = pd.to_datetime(ted_talks_df['film_date'], unit='s')
ted_talks_df['published_date'] = pd.to_datetime(ted_talks_df['published_date'], unit='s')
print('Average days between filming and publishing : ',
      (ted_talks_df['published_date'] - ted_talks_df['film_date']).dt.days.mean())
ted_talks_df['days_til_now'] = (dt.today()-ted_talks_df['published_date']).dt.days



# Q-1-e
# Unpacking the ratings column
rating_df = pd.DataFrame()
for i in range(ted_talks_df.shape[0]):
    temp_df = pd.DataFrame(ast.literal_eval(ted_talks_df['ratings'][i]))
    temp_df['title'] = ted_talks_df['title'][i]
    temp_df['days_til_now'] = ted_talks_df['days_til_now'][i]
    temp_df['views'] = ted_talks_df['views'][i]
    rating_df = pd.concat([rating_df, temp_df])
    
rating_df.reset_index(inplace=True)



# Q-1-f
# Total ratings received by each talk
count_rating = rating_df.groupby('title', as_index=False).sum()[['title', 'days_til_now', 'count', 'views']]
print(count_rating.head())


# Percentage of negative ratings
neg_rating = rating_df[rating_df['id'].isin([21,2,26,11])].groupby('title', as_index=False).sum()[['title', 'count']]
count_rating = pd.merge(count_rating, neg_rating, left_on='title', right_on='title')
count_rating['percent_neg_rating'] = count_rating['count_y'] *100 /count_rating['count_x']

# Average ratings per day after publishing
count_rating['avg_per_day'] = count_rating['count_x']/count_rating['days_til_now']
print(count_rating[['title', 'percent_neg_rating', 'avg_per_day']].head())



# Q-1-g
# Which talks were the funniest
funny_titles = rating_df[rating_df['id']==7].sort_values('count', ascending=False)['title'][:5]
print(pd.merge(funny_titles, ted_talks_df, left_on='title', right_on='title')[['speaker_occupation']])
print('Data Scientist at 5th position, surpsrising..!')

# Most frequent rating categoy for each talk
freq_df = rating_df.groupby('title').apply(lambda x : rating_df['name'][x['count'].idxmax()])
print(freq_df.head())

# Keeping the first entry in the occupation column
ted_talks_df.loc[ted_talks_df['speaker_occupation'].isnull(), 'speaker_occupation'] = 'Unknown'
ted_talks_df['speaker_occupation'] = ted_talks_df['speaker_occupation']\
                                    .apply(lambda x : x.split(',')[0].split('/')[0].split(';')[0])

# Q-1-d
# Best events in ted_talks_df history - according to the 
# Two parameters are considered - % negative ratings and total views (measure of popularity)
best_events = count_rating[count_rating['percent_neg_rating']<5.0]\
              .sort_values('views', ascending=False)[['title', 'views', 'percent_neg_rating']]