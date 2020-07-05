import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['January', 'February', 'March', 'April', 'May', 'June']
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while True:
        try:
            city = input('Would you like to see data for Chicago, New York City, or Washington?\n')
            city = city.lower()
            CITY_DATA[city]
            break
        except KeyError:
            print("Oops! '{}' is not one of the three cities. Check spelling and try again... ".format(city.title()))
        except KeyboardInterrupt:
            print('That was not a valid input. Try again...')

    # get filter for data
    print()
    filters = ['month', 'day', 'both', 'none']

    while True:
        try:
            filter = input('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.\n')
            filter = filter.lower()
            filters.index(filter)
            break
        except ValueError:
            print("Oops! '{}' is not a valid filter. Try again... ".format(filter))
        except KeyboardInterrupt:
            print('That was not valid filter. Try again...')

    print()
    month = 'all'
    day = 'all'

    # get input for month
    if filter == 'month' or filter == 'both':
        while True:
            try:
                month = input('Which month? {}, {}, {}, {}, {}, or {}?\n'.format(*months))
                month = month.title()
                months.index(month)
                print()
                break
            except ValueError:
                print("Oops! '{}' is not a valid input. Try again... ".format(month))
            except KeyboardInterrupt:
                print('That was not a valid input. Try again...')

    # get input for day of week
    if filter =='day' or filter == 'both':
        while True:
            try:
                day = input('Which day? {}, {}, {}, {}, {}, {}, {}?\n'.format(*days))
                day = day.title()
                days.index(day)
                break
            except ValueError:
                print("Oops! '{}' is not a valid input. Try again... ".format(day))
            except KeyboardInterrupt:
                print('That was not a valid input. Try again...')

    print('-'*40)
    return city, month, day, filter


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] =  df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month.title()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df, filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if filter == 'none' or filter == 'day':
        popular_month = df['month'].value_counts().idxmax()
        popular_month_count = df['month'].value_counts().max()
        print('Most Frequent Start Month:{}, Count:{}, Filter:{}'.format(months[popular_month-1], popular_month_count, filter))

    # display the most common day of week
    if filter == 'none' or filter == 'month':
        popular_day_of_week = df['day_of_week'].value_counts().idxmax()
        popular_day_of_week_count = df['day_of_week'].value_counts().max()
        print('Most Frequent Day of Week:{}, Count:{}, Filter:{}'.format(popular_day_of_week, popular_day_of_week_count, filter))

    # display the most common start hour
    popular_hour = df['hour'].value_counts().idxmax()
    popular_hour_count = df['hour'].value_counts().max()
    print('Most Frequent Start Hour:{}, Count:{}, Filter:{}'.format(popular_hour, popular_hour_count, filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df, filter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    popular_start_station_count = df['Start Station'].value_counts().max()
    print('Most Commonly Used Start Station:{}, Count:{}, Filter:{}'.format(popular_start_station, popular_start_station_count, filter))

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    popular_end_station_count = df['End Station'].value_counts().max()
    print('Most Commonly Used End Station:{}, Count:{}, Filter:{}'.format(popular_end_station, popular_end_station_count, filter))

    # display most frequent combination of start station and end station trip
    popular_comb = df.groupby(['Start Station','End Station']).size().idxmax()
    popular_comb_count = df.groupby(['Start Station','End Station']).size().max()
    print('Most Frequent Combination of Start Station and End Station:{}, Count:{}, Filter:{}'.format(popular_comb, popular_comb_count, filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df, filter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel and mean travel times
    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()
    trips_count = df['Trip Duration'].count()
    print('Total Duration:{}, Mean Duration:{}, Trips Count:{}, Filter:{}'.format(total_travel_time,mean_travel_time,trips_count, filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, filter):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('Users Breakdown (Filter:{}):'.format(filter))
    for i in range(len(user_type_count)):
        print('{}: {}'.format(user_type_count.index[i], user_type_count.values[i]))

    # Display counts of gender
    print()
    print('Gender Breakdown (Filter:{}):'.format(filter))
    if 'Gender' not in df.columns:
        print('No gender data.\nNone')
    else:
        gender_count = df['Gender'].value_counts()
        for i in range(len(gender_count)):
            print('{}: {}'.format(gender_count.index[i], gender_count.values[i]))

    # Display earliest, most recent, and most common year of birth
    print()
    print('Earliest, most recent, and most common year of birth (Filter:{}):'.format(filter))
    if 'Birth Year' not in df.columns:
        print('No birth year data.\nNone')
    else:
        earliest_year = int(df['Birth Year'].min())
        latest_year = int(df['Birth Year'].max())
        birth_year_mode = int(df['Birth Year'].value_counts().idxmax())
        print('Earliest Year:{} \nMost Recent Year:{} \nMost Common Year:{}'.format(earliest_year, latest_year, birth_year_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df):
    """Asks user whether they would like to see raw data and prints 5 rows at a time."""
    # print all columns
    pd.set_option('display.max_columns',None)

    # remove month, hour, and day of week columns from the dataframe
    df1 = df.drop(['month','hour','day_of_week'], axis = 1)

    raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
    if raw_data.lower() == 'yes':
        i = 0
        while i <= len(df1.index) - 5:
            print(df1[i:i+5])
            i += 5
            raw_data = input('\nWould you like to see 5 more rows of data? Enter yes or no.\n')
            if raw_data.lower() != 'yes':
                break

def main():
    while True:
        city, month, day,filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df,filter)
        station_stats(df,filter)
        trip_duration_stats(df, filter)
        user_stats(df, filter)
        print_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
