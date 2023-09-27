from datetime import timedelta

import pandas as pd

from db.base import engine


def import_data():
    df = pd.read_csv('hotel_booking_data.csv')

    df_tosql = pd.DataFrame(columns=['id', 'booking_date', 'length_of_stay', guest_name, 'daily_rate'])
    df_tosql['booking_date'] = df['arrival_date_year'].astype(str) + '-' + df['arrival_date_month'].astype(str) + '-' + \
                               df['arrival_date_day_of_month'].astype(str)

    df_tosql['length_of_stay'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df_tosql['guest_name'] = df['name']
    df_tosql['daily_rate'] = df['adr']
    df_tosql['id'] = df_tosql.index

    df_tosql.to_sql('bookings', con=engine, if_exists='append', index=False)


def import_df():
    df = pd.read_csv('hotel_booking_data.csv')
    month_mapping = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
    df['numerical_date'] = pd.to_datetime(df['arrival_date_year'].astype('str') + df['arrival_date_month'].map(
        month_mapping).astype('str') + df['arrival_date_day_of_month'].astype('str'), format='%Y%m%d')
    df['arrival_week_day'] = df['numerical_date'].dt.day_name()
    df.drop('numerical_date', axis=1, inplace=True)
    df['arrival_date_year'].astype('str')
    df['arrival_date'] = df['arrival_date_year'].astype('str') + '-' + df['arrival_date_month'] + '-' + df[
        'arrival_date_day_of_month'].astype('str')
    df['arrival_date'] = pd.to_datetime(df['arrival_date'])
    df['booking_date'] = df['arrival_date'] - df['lead_time'].apply(lambda x: timedelta(days=x))
    df['arrival_date'] = df['arrival_date'].dt.strftime('%Y-%m-%d')
    df['booking_date'] = df['booking_date'].dt.strftime('%Y-%m-%d')
    df['booking_date'] = pd.to_datetime(df['booking_date'])
    df['booking_year'] = df['booking_date'].dt.year
    df['booking_month'] = df['booking_date'].dt.month
    df['length_of_stay'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df.drop(columns=['arrival_date_day_of_month', 'arrival_date_week_number', 'stays_in_weekend_nights',
                     'stays_in_week_nights'], inplace=True)


    return df



