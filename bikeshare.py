import time
import pandas as pd

CITY_DATA = {"CH": 'chicago.csv', "NY": 'new_york_city.csv', "WA": 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('#' * 45)
    print('Hello! Let\'s explore some US bike share data!')
    print('#' * 45)

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities_data = ["CH", "NY", "WA"]
    print(cities_data)
    city = input("please choose city from a list above?    ").upper().strip()
    while city not in cities_data:
        print('you type invalid inputs!!')
        print(cities_data)
        city = input("please choose city from a list above?    ").upper().strip()

    # get user input for filter (month, day or both)

    filtering = input("would you like to filter data by month, day, both or none?   ").lower().strip()
    while filtering not in (['month', 'day', 'both', 'none']):
        filtering = input("would you like to filter data by month, day, both or none?   ").lower().strip()
        print('you type invalid inputs!!')
    # get user input for month (all, january, february, ... , june)

    if filtering == "month" or filtering == "both":
        months = ["jan", "feb", "mar", "apr", "may", "jun"]
        print(months)
        month = input("please choose month?    ").lower().strip()
        while month not in months:
            print('you type invalid inputs!!')
            print(months)
            month = input("please choose month date?    ").lower().strip()
    else:
        month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filtering == "day" or filtering == "both":
        days_data = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
        print(days_data)
        day = input("please choose day?    ").lower().strip()
        while day not in days_data:
            print('you type invalid inputs!!')
            print(days_data)
            day = input("please choose day or all?    ").lower().strip()
    else:
        day = 'all'

        print('-' * 40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time dt'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time dt'].dt.month
    df['day_of_week'] = df['Start Time dt'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ["jan", "feb", "mar", "apr", "may", "jun"]
    month = df["month"].mode()[0]
    print(f"the most common month is: {months[month - 1]} ")
    # display the most common day of week

    day = df["day_of_week"].mode()[0]
    print(f"the most common day is: {day} ")

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    top_start_station = df["Start Station"].mode()[0]
    print(f"the most commonly used start station is: {top_start_station} ")
    # display most commonly used end station
    top_end_station = df["End Station"].mode()[0]
    print(f"the most commonly used end station is: {top_end_station} ")

    # display most frequent combination of start station and end station trip
    top_trip = df["Start Station"] + ['to'] + df["End Station"]
    print(f"the most commonly trip is: {top_trip.mode()[0]} ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_durations = ((pd.to_datetime(df['End Time'])) - (pd.to_datetime(df['Start Time']))).sum()
    days = total_travel_durations.days
    hours = total_travel_durations.seconds // (60 * 60)
    minutes = total_travel_durations.seconds % (60 * 60) // 60
    seconds = total_travel_durations.seconds % (60 * 60) % 60
    print(f"total travel time is: {days} days, {hours} hours, {minutes} minutes and {seconds} seconds.")

    # display mean travel time
    travel_durations_mean = ((pd.to_datetime(df['End Time'])) - (pd.to_datetime(df['Start Time']))).mean()
    days = travel_durations_mean.days
    hours = travel_durations_mean.seconds // (60 * 60)
    minutes = travel_durations_mean.seconds % (60 * 60) // 60
    seconds = travel_durations_mean.seconds % (60 * 60) % 60
    print(f"travel_durations_average is: {days} days, {hours} hours, {minutes} minutes and {seconds} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def user_stats(df):
    """Displays statistics on bike share users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    print(df['User Type'].value_counts())
    print('-' * 40)

    # Display counts of gender
    if "Gender" in df.columns:
        print(df['Gender'].value_counts())
        print('-' * 40)
    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print('most earliest year of birth:')
        print(int(df['Birth Year'].min()))
        print('most recent year of birth:')
        print(int(df['Birth Year'].max()))
        print('most common year of birth:')
        print(int(df['Birth Year'].mode()[0]))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)

def data_view(df):
    data_show = input("would you like to view data?      ").lower().strip()
    if data_show == "yes":
        count = 0
        while True:
            print(df.iloc[count: count+5])
            count += 5
            data_show_more = input("you want view more data?   ").lower().strip()
            if data_show_more != "yes":
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_view(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
