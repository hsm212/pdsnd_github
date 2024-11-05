#importing necessary libraries
import time
import pandas as pd
import numpy as np
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington)
    city = input('Enter city: ').lower()
    while city not in CITY_DATA.keys():
        print(f'Invalid city. Please enter {", ".join(CITY_DATA.keys())}.')
        city = input('Enter city: ').lower()

    # Get user input for month (all, january, february, ... , june)
    month = input('Enter month: ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        print(f'Invalid month. Please enter "all" or one of the following: {", ".join(["january", "february", "march", "april", "may", "june"])}.')
        month = input('Enter month: ').lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter day: ').lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        print(f'Invalid day. Please enter "all" or one of the following: {", ".join(["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])}.')
        day = input('Enter day: ').lower()

    print('-'*40)
    return city, month, day

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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.strftime("%B").str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # Filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    if len(df['month'].unique()) > 1:
        common_month = df['month'].mode()[0]
        print('Most Common Month:', common_month)

    # Display the most common day of week
    if len(df['day_of_week'].unique()) > 1:
        common_day_of_week = df['day_of_week'].mode()[0]
        print('Most Common Day of Week:', common_day_of_week)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', common_start_station)

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', common_end_station)

    # Display most frequent combination of start station and end station trip
    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Frequent Combination of Start Station and End Station Trip:', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of Gender:\n', gender_counts)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print('\nEarliest Year of Birth:', earliest_year)
        print('Most Recent Year of Birth:', most_recent_year)
        print('Most Common Year of Birth:', most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        # Get user input for city, month, and day
        city, month, day = get_filters()
        
        # Load data for the specified city and filters
        df = load_data(city, month, day)

        # Display statistics on the most frequent times of travel
        time_stats(df)
        
        # Display statistics on the most popular stations and trip
        station_stats(df)
        
        # Display statistics on the total and average trip duration
        trip_duration_stats(df)
        
        # Display statistics on bikeshare users
        user_stats(df)

        # Ask user if they want to view raw data (5 rows at a time)
        index = 0  # Start from the first row of data. 0-indexed. 5 rows per iteration.
        while True and index < len(df): 
            view_raw_data = input('\nWould you like to view raw data? Enter yes or no.\n')
            if view_raw_data.lower() == 'yes':
                print(df[index:index+5])
                if(index+5 < len(df)):
                    index += 5
                elif ((len(df) - index) > 0):
                    print(df[index:])
                else:
                    print('No more data to display.')
                    break
            # Ask user if they want to restart the program
            if view_raw_data.lower() != 'yes':
                break

        # Ask user if they want to restart the program
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

# Entry point of the program
if __name__ == "__main__":
    main()