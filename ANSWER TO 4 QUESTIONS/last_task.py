import pandas as pd

from funcs import import_df

df = pd.read_csv('hotel_booking_data.csv')

# 1 task
most_popular_last_names = df['name'].str.split().str[-1].str.replace('MD', 'Last_Name_MD').value_counts().head()
print(most_popular_last_names)

# 2 task
name_people_booked_most_number_kids = df[df['children'] + df['babies'] == df['children'].add(df['babies']).max()][
    'name']
print(name_people_booked_most_number_kids)

# 3 task
arrival_bet_1_and_15 = df[
    (df['arrival_date_day_of_month'].astype('int') >= 1) & df['arrival_date_day_of_month'].astype('int') <= 15].sum()
print(arrival_bet_1_and_15)

#4 task
df = import_df()
week_days = df['arrival_week_day'].value_counts()
print(week_days)
