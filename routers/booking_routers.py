from typing import List, Optional, Dict, Annotated

from fastapi import APIRouter, Depends, status, Query, Path
from starlette.responses import Response

from crud.db_crud import BookingCRUD
from db.tables import Bookings
from funcs import import_df
from models.models_db import BookingOutORM, BookingIn

from auth.auth import user_enter

bookings_db = APIRouter(
    prefix='/bookings',
    tags=['Basic database techniques']
)

search = APIRouter(
    prefix='/bookings/search',
    tags=['Searching some data in database']
)

analysis = APIRouter(
    prefix='/bookings/analysis',
    tags=['''Performs advanced analysis on the dataset, 
    generating insights and trends based on specific criteria''']
)

stats = APIRouter(
    prefix='/bookings/stats',
    tags=['Provides statistic information about the dataset']
)


@bookings_db.get('', response_model=List[BookingOutORM],
                 status_code=status.HTTP_200_OK,
                 description="Returns all data from database")
async def all_from_database(limit: int = Query(100, le=100),
                            offset: int = Query(0),
                            booking_crud: BookingCRUD = Depends()):
    return booking_crud.get_all(limit, offset)


@bookings_db.post('/new', response_model=BookingOutORM,
                  status_code=status.HTTP_201_CREATED,
                  description='Creating new entity for database and adding it')
async def new_entity(data: BookingIn,
                     booking_crud: BookingCRUD = Depends()):
    ent = booking_crud.create_new(dict(data))
    return ent


@bookings_db.delete('/delete', response_model=BookingOutORM,
                    status_code=status.HTTP_202_ACCEPTED,
                    description='Delete one booking from database by id')
async def delete_booking_by_id(booking_id: int = Query(ge=0),
                               booking_crud: BookingCRUD = Depends()):
    data = booking_crud.delete(booking_id)
    return data


@search.get('/{bookings_id}', response_model=BookingOutORM,
            status_code=status.HTTP_200_OK,
            description='Get data from database by booking id')
async def get_by_id(bookings_id: int = Path(ge=0),
                    booking_crud: BookingCRUD = Depends()):
    data = booking_crud.get_one(bookings_id)
    return data


@search.get('', response_model=List[BookingOutORM],
            status_code=status.HTTP_200_OK,
            description='Returns a booking list based on parameters')
async def get_by_param(booking_date: Optional[str] = None,
                       length_of_stay: Optional[int] = None,
                       guest_name: Optional[str] = None,
                       daily_rate: Optional[float] = None,
                       booking_crud: BookingCRUD = Depends()):
    data = booking_crud.search(booking_date, length_of_stay, guest_name, daily_rate)
    return data


@analysis.get('/nationality', response_model=List[BookingOutORM],
              status_code=status.HTTP_200_OK,
              description='Returns bookings matching the provided nationality')
async def get_by_nationality(nationality: str = Query(min_length=3),
                             limit: int = Query(100, le=100),
                             offset: int = Query(0, ),
                             df: import_df = Depends()):
    nationality = nationality.upper()
    data = df[df['country'] == nationality].iloc[offset:limit]
    return Response(data.to_json(orient='records'), media_type='application/json')


@analysis.get('/popular_meal_package',
              status_code=status.HTTP_200_OK,
              description='Returns the most popular meal in bookings')
async def get_most_popular_meal(df: import_df = Depends()):
    data = df['meal'].value_counts().to_dict()
    max_val_in_data = max(data.values())
    result = [k for k in data.items() if k[1] == max_val_in_data][0]
    return {'Most popular meal is': result[0] + '- count:' + str(result[1])}


@analysis.get('/total_revenue', response_model=List[BookingOutORM],
              status_code=status.HTTP_200_OK,
              description='Returns total revenue for each booking type and month')
async def total_revenue_of_booking_month_and_hotel(df: import_df = Depends()):
    data = df.groupby(['hotel', 'arrival_date_month']).agg({'adr': 'sum'}).reset_index()
    return Response(data.to_json(orient='records'), media_type='application/json')


@analysis.get('/top_countries',
              status_code=status.HTTP_200_OK,
              description='Returns 5 countries with the most bookings')
async def top_5_countries(df: import_df = Depends()):
    data = df['country'].value_counts().head(5)
    return data.to_dict()


@analysis.get('/total_guest_by_year',
              status_code=status.HTTP_200_OK,
              description='Returns total number of guests by year')
async def total_guests_year(df: import_df = Depends()):
    df['sum_people'] = df[['adults', 'children', 'babies']].sum(axis=1)
    data = df.groupby(['arrival_date_year']).agg({'sum_people': 'sum'}).reset_index()
    return Response(data.to_json(orient='records'), media_type='application/json')


@analysis.get('/most_common_arrival_day_city', response_model=Dict[str, str],
              status_code=status.HTTP_200_OK,
              description='Returns the most common arrival date of the week for city hotel')
async def most_com_day_of_week(credentials: Annotated[str, Depends(user_enter)],
                               df: import_df = Depends()):
    df = df[df['hotel'] == 'City Hotel']
    week_day = df['arrival_week_day'].value_counts().idxmax()
    return {"Most common arrival day of week is": week_day}


@stats.get('/avg_length_of_stay',
           status_code=status.HTTP_200_OK,
           description='''Returns average length of stay for each combination 
           of booking year and hotel type''')
async def avg_len_of_stay(df: import_df = Depends()):
    data = df.groupby(['hotel', 'booking_year']).agg({'length_of_stay': 'mean'}).reset_index()
    return Response(data.to_json(orient='records'), media_type='application/json')


@stats.get('/repeated_guests',
           status_code=status.HTTP_200_OK,
           description='Returns percentage of repeated guests')
async def repeated_guests_per(df: import_df = Depends()):
    data = df.groupby('is_repeated_guest')['is_repeated_guest'].apply(lambda x: x == 1).mean() * 100
    return {'Percentage of repeated guests is:': data}


@stats.get('/avg_daily_rate_resort',
           status_code=status.HTTP_200_OK,
           description='Returns the average daily rate by month for resort hotel bookings')
async def avg_daily_rate_resort(credentials: Annotated[str, Depends(user_enter)],
                                df: import_df = Depends()):
    df = df[df['hotel'] == 'Resort Hotel']
    data = df.groupby(['booking_month']).agg({'adr': 'mean'}).reset_index()
    return Response(data.to_json(orient='records'), media_type='application/json')


@stats.get('/count_by_hotel_repeated_guests',
           status_code=status.HTTP_200_OK,
           description='Returns count of bookings by hotel type and repeated guests')
async def count_rep_guests_by_hotel(credentials: Annotated[str, Depends(user_enter)],
                                    df: import_df = Depends()):
    data = df.groupby(['hotel', 'is_repeated_guest']).size().reset_index()
    return Response(data.to_json(orient='records'), media_type='application/json')


@stats.get('/total_revenue_resort_by_country',
           status_code=status.HTTP_200_OK,
           description='Returns total revenue by country for resort hotel bookings')
async def total_rev_res_by_country(credentials: Annotated[str, Depends(user_enter)],
                                   df: import_df = Depends()):
    df = df[df['hotel'] == 'Resort Hotel']
    data = df.groupby('country').agg({'adr': 'sum'}).reset_index()
    return Response(data.to_json(orient='records'), media_type='application/json')


@stats.get('/count_by_hotel_meal',
           status_code=status.HTTP_200_OK,
           description='Returns count of bookings by hotel type and meal package')
async def count_by_hotel_and_meal(credentials: Annotated[str, Depends(user_enter)],
                                  df: import_df = Depends()):
    data = df.groupby(['hotel', 'meal']).size().reset_index()
    return Response(data.to_json(orient='records'), media_type='application/json')
