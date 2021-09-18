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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('Which city are you interested in:\n').lower()
    while city not in ['chicago','new york city','washington']:
        city = input('Please choose one of the following cities: chicago, new york city, washington, or enter X to quit:\n').lower()
        if city == 'x':
            quit()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Please select a month from january to june or enter "all" for all months:\n').lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june','all']:
        month = input('Please select a month from january to june or enter "all" for all months:\n').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please select a day of week or enter "all" for all days:\n').lower()
    while day not in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','all']:
        day = input('Please select a day or enter "all" for all days:\n').lower()


    print('-'*40)
    return city,month,day


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

    df = pd.read_csv(CITY_DATA[city])

    #convert datetime columns to datetime data type for better processing..
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #make 2 new columns for "month" & "day of the week" out of "Start Time" column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        # get month's id and create a new dataframe filtered by month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month']==month]


    if day != 'all':
        # create a new dataframe filtered by day
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('\nthe most common month: {}' . format(df['month'].mode()[0]))


    # TO DO: display the most common day of week
    print('\nthe most common day of week: {}' . format(df['day_of_week'].mode()[0]))


    # TO DO: display the most common start hour
    print('\nthe most common start hour: {}' . format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('\nthe most common Start Station: {}' . format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('\nthe most common End Station: {}' . format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    #Ref: https://stackoverflow.com/questions/55719762/how-to-calculate-mode-over-two-columns-in-a-python-dataframe
    res = (df['Start Station'] + ' <-> ' + df['End Station']).mode()[0]
    print('\nthe most common combination of Start & End Stations: {}' . format(res))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    #Ref: https://queirozf.com/entries/python-number-formatting-examples
    print('\nThe total travel time (in hours): {:,.2f}' . format(df['Trip Duration'].sum()/3600))

    # TO DO: display mean travel time
    print('\nThe mean travel time is (in minutes): {:.2f}' . format(df['Trip Duration'].mean()/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('\nCounts of user types:\n')
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    #note: no gender in washington dataset
    try:
        print('\nCounts per gender:\n')
        print('Male: {:,d}' . format(df['Gender'].value_counts()[0]))
        print('Female: {:,d}' . format(df['Gender'].value_counts()[1]))
        #print('\nCounts of gender: {}' . format(df['Gender'].value_counts()))
    except KeyError:
        print("\nGender details are not available in this dataset!.")

    # TO DO: Display earliest, most recent, and most common year of birth
    #note: no Birth Year in washington dataset
    try:
        print('\nEarliest year of birth: {}'.format(int(df['Birth Year'].min())))
        print('\nMost recent year of birth: {}'.format(int(df['Birth Year'].max())))
        print('\nMost common year of birth: {}'.format(int(df['Birth Year'].mode()[0])))
    except KeyError:
        print("\nBirth Year details are not available in this dataset!.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def rawdata_display(df,city):
    """Displays statistics on bikeshare users."""
    #df =df[1:] #ignore first column
    print('\nRawdata Display...\n')
    datadisp = input('Do you want to browse the first 5 rows of "{}" dataset? [Y/N]'.format(city))
    i=0
    while (datadisp.lower() =='y') and (i<df.shape[0]):
        #display next 5 rows and ignore the first column as it's unuseful
        print(df.iloc[i:i+5,1:])
        i+=5
        datadisp = input('Display the next 5 rows? [Y/N]:\n')
        if datadisp.lower() == 'n':
            quit()

    return

def main():
    while True:
        city, month, day = get_filters()
        print('{} - {} - {}' . format(city, month, day))
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        rawdata_display(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
