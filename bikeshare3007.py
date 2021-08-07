import pandas as pd
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

DAYS_OF_WEEK = ['monday', 'tuesday', 'wednesday', 'tuesdays', 'thursday', 'friday', 'saturday', 'sunday']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek


    # filter by month if applicable,check condition for ALL
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = DAYS_OF_WEEK.index(day) + 1

        # filter by day to create the new dataframe
        df = df[df['day_of_week'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Convert Start Time column to datetime object
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    common_day = DAYS_OF_WEEK[df['day_of_week'].mode()[0] - 1]
    print("Most common day of week is: ", common_day)

    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"Most populor hour was: {popular_hour}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station=df["Start Station"].mode()[0]
    print("most commonly used start station:\n",most_common_start_station)


    # display most commonly used end station
    most_common_end_station=df["End Station"].mode()[0]
    print("most commonly used end station:\n",most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[["Start Station", "End Station"]].agg(' -> '.join, axis=1)

    print("Most Common Trips is:\n",most_common_start_end_station.mode()[0])    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("total travel duration in HH:MM:SS format is: ", time.strftime("%H:%M:%S", time.gmtime(df["Trip Duration"].sum())))

    # display mean travel time
    print("Mean travel duration in HH:MM:SS format is: ", time.strftime("%H:%M:%S", time.gmtime(df["Trip Duration"].mean())))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df["User Type"].value_counts()
    print("Count per user types are:\n",count_user_types, "\n\n")

    # Display counts of gender
    if city != 'washington':
        count_gender = df["Gender"].value_counts()
        print("User gender count:\n", count_gender, "\n\n")

    # Display earliest, most recent, and most common year of birth
        earliest_birth = df["Birth Year"].min()
        latest_birth=df["Birth Year"].max()
        most_common_year=df["Birth Year"].mode()[0]
        print("Earliest birth year is: ",earliest_birth)
        print("Latest birth year is: ", latest_birth)
        print("most common birth year is: ", most_common_year)
    else:
        print("Washington city doesn't have gender and birthyear data present")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#from here main function begins

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        check= input('\n Would you like to see raw data? Enter yes or no.\n').lower()
        if check =='yes':
            while check =='yes':
                i = int(input ('\n how many rows do you want to see.\n'))
                print(df.head(i))
                check= input('\n do you wish to see more raw data? Enter yes or no.\n').format(i).lower()
        else:
            print('\n Printing full data:\n',df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    
def get_filters():
    city = input("Enter your City:\n").lower()

    # To check entered city is valid
    while city not in CITY_DATA.keys():
        city = input("City is not available, Please enter again:\n").lower()
    USER_INPUT= ['day','month','both','none']
    filter_by = input("Which way would you like to filter you data by ? Day, Month, Both or none.\n").lower()
    
    if filter_by not in USER_INPUT:
        while filter_by not in USER_INPUT:
            print("Invalid input provided,please enter again \n")
            filter_by = input("Which way would you like to filter you data by ? Day, Month, Both or none.\n").lower()

    if filter_by == "day":
        day = input(f"Enter your Day from {DAYS_OF_WEEK}:\n").lower()
        month = "all"
        while day not in days_of_week:
            day = input(f"Invalid day,please enter day from {DAYS_OF_WEEK}:\n").lower()
    elif filter_by == "month":
        day = "all"
        month = input(f"Enter your month from {MONTHS}:\n").lower()
        while month not in MONTHS:
            month = input(f"Invalid month,please enter valid month again:\n").lower()
    elif filter_by == "both":
        month = input(f"Enter your month from {MONTHS}:\n").lower()
        while month not in MONTHS:
            month = input(f"Invalid month,please enter valid month again:\n").lower()
        day = input(f"Enter your Day from {DAYS_OF_WEEK}:\n").lower()
        while day not in days_of_week:
            day = input(f"Invalid day,please enter day from {DAYS_OF_WEEK}:\n").lower()
        
    elif filter_by == "none":
        day = "all"
        month = "all"
        
    return city, month, day

if __name__ == "__main__":
	main()
