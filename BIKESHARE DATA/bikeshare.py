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
    city = str(input('Please enter the input for the city[no caps] : '))
    while(not(city in CITY_DATA)):
        city = str(input('The entered city data is not available , please try another city[no caps] :'))
        if city in CITY_DATA:
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all','january','february','march','april','may','june']
    month = str(input('Please input the month to be applied as filter[no caps] : '))
    while(not(month in months)):
        month = str(input('The entered month data is not available/invalid , please try another month between january and june[no caps] :'))
        if month in months:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day = str(input('Please input the day of the week :'))
    while(not(day in days)):
        day = str(input('The entered day is invalid , please enter correct day[no caps] :'))
        if day in days:
            break
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
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        
        # filter by month to create the new dataframe
        df = df[df['month']==month]
        
    # filter by day of week if applicable
    if day != 'all':
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        day = days.index(day.title())
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january','february','march','april','may','june']
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # TO DO: display the most common month
    cm = df['month'].mode()[0]
    print('\n The most common month is {}\n'.format(months[cm-1]))

    # TO DO: display the most common day of week
    cd = df['day_of_week'].mode()[0]
    print('\n The most common day is {}\n'.format(cd))

    # TO DO: display the most common start hour
    df['start hour']=df['Start Time'].dt.hour
    ch= df['start hour'].mode()[0]
    print('\n The most common start hour is {}\n'.format(ch))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    cuss = df['Start Station'].mode()[0]
    print('\n most common starting station :{}\n'.format(cuss))
   
    # TO DO: display most commonly used end station
    cues = df['End Station'].mode()[0]
    print('\n most common Ending station :{}\n'.format(cues))

    # TO DO: display most frequent combination of start station and end station trip
    df['start&end']=  df["Start Station"].astype(str) + " to " + df["End Station"].astype(str)
    cuses=df['start&end'].mode()[0]
    print('\n most frequent combination of start station and end station trip :{}\n'.format(cuses))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    sum = df['Trip Duration'].sum()
    print('\n calculated total travel time is {}\n'.format(sum))

    # TO DO: display mean travel time
    mean = df['Trip Duration'].mean()
    print('\n calculated mean travel time is {}\n'.format(mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('\ncount of all user types is shown below : \n')
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print('\ncount of all Gender is shown below : \n')
        print(df['Gender'].value_counts())
    else:
        print('\n The city file does not have gender data\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\n Earliest year of birth was found to be {}\n'.format(int(df['Birth Year'].min())))
        print('\n Most recent year of birth was found to be {}\n'.format(int(df['Birth Year'].max())))
        print('\n Most common year of birth was found to be {}\n'.format(int(df['Birth Year'].mode()[0])))
    else:
        print('\n The city file does not have year of birth data\n')
        
    # Display individual data of five's
    choices = ['yes' , 'no']
    choice = str(input('\n Would like to see the data for first five indiviual users[yes/no] : ')).lower()
    while(not(choice in choices)):
        choice = str(input('\n The entered choice is invalid please enter the correct choice[yes/no] :')).lower()
        if choice in choices:
            break
            
    
    i=5
    x=0
    while(choice == 'yes'):
        
        print(df[x:i])
        choice = str(input('\n Would like to see the individual data for next five indiviual users[yes/no] : ')).lower()
        while(not(choice in choices)):
            
            choice = str(input('\n The entered choice is invalid please enter the correct choice[yes/no] :')).lower()
            if choice in choices:
                
                break
        x=i
        i += 5
        if choice == 'no':
            break
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
   
  


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
