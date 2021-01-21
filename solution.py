import time
import pandas as pd
import numpy as np

# Dictionary for Country Name and Data Filtering
CITY_DATA = {'chicago': 'chicago.csv',
			 'new york': 'new_york_city.csv',
			 'new york city': 'new_york_city.csv',
			 'washington': 'washington.csv'}
months = ["january", "february", "march", "april", "may", "june"]

def get_filters():
    
    """Asks user to specify a city, month, and day to analyze.
    city = 
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please enter a CITY name: Chicago, New York, or Washington\n").lower()

    # Filter : Month, Day, Both, or None
    fl = input('Would you like to Filter by : Month, Day, Both, or None?\n').lower()
    if fl == "both":
        month = input('Which month? January, February, March, April, May or June?\n').lower()
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday\n").title()
    elif fl == "month":
        month = input('Which month? January, February, March, April, May or June\n')
        day = None
    elif fl == "day":
        month = None
        day = input("Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday\n").title()
    else:
    	month = day = fl = None
    print('-'*40)

    return city, month, day, fl

# Load dataframe
def load_data(city, month, day, fl):
    while True:
        try:
            df = pd.read_csv(CITY_DATA[city])
        except Exception as e:
            print("{} is not among the city name!".format(city))
            city, month, day, fl = get_filters() 
            #raise
        else:
            break
        finally:
            pass

    #df = pd.read_csv(CITY_DATA[city]) #use try excp = is not among the city
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    # Filter
    if month != None:
        # df ==> filter by month
        month_index = months.index(month) + 1
        #print("month int: {}".format(month))
        df = df[df["month"] == month_index]
        #count_month = df[df["month"] == month_index]["month"].count()
        #print("month: {}, count: {}, Filter: {}".format(month, count_month, fl.title()))

    if day != None: 
        df = df[df['day_of_week'] == day.title()]
		#count_day = df[df["day_of_week"] == day.title()]["day_of_week"].count()
		#print("Day: {}, count: {}, Filter: {}".format(day, count_day, fl.title()))
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_int = df['month'].mode()[0]
    com_month = months[month_int - 1]
    count_com_month = df[df["month"] == month_int]["month"].count()
    print("Common Month: {}, Count: {}, Filter: {}".format(com_month,count_com_month,fl))

    # display the most common day of week
    com_day = df['day_of_week'].mode()[0]
    count_com_day = df[df["day_of_week"] == com_day.title()]["day_of_week"].count()
    print("Common Day: {}, Count: {}, Filter: {}".format(com_day,count_com_day,fl))


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    com_hour = df['hour'].mode()[0]
    count_com_hour = df[df['hour'] == com_hour]['hour'].count()
    print("Common Hour: {}, Count: {}, Filter: {}".format(com_hour,count_com_hour,fl))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    com_start_station = df['Start Station'].mode()[0]
    count_com_start_stat = df[df['Start Station']==com_start_station]['Start Station'].count()
    print("Common Start Station: {}, Count: {}, Filter: {}".format(com_start_station,count_com_start_stat,fl))
    # display most commonly used end station
    com_end_station = df['End Station'].mode()[0]
    count_com_end_stat = df[df['End Station'] == com_end_station]['End Station'].count()
    print("Common End Station: {}, Count: {}, Filter: {}".format(com_end_station,count_com_end_stat,fl))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " ==> " + df['End Station']
    com_trip = df['Trip'].mode()[0]
    count_com_trip = df[df['Trip'] == com_trip]['Trip'].count()
    print("Common Trip: {}, Count: {}, Filter: {}".format(com_trip, count_com_trip,fl))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip = df['Trip Duration'].sum()
    
    # Count
    count_trip = df['Trip Duration'].count()

    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()

    # Print
    print("Total Trip Duration is: {}, Count: {}, Avg Duration: {}, Filter: {}".format(total_trip,count_trip, mean_trip_duration,fl))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
	"""Displays statistics on bikeshare users."""
	print('\nCalculating User Stats...\n')
	start_time = time.time()

	# Display counts of user types
	#print('Stats for "User Type" ...')
	count_subsc = df[df['User Type'] == 'Subscriber']['User Type'].count()
	count_custo = df[df['User Type'] == 'Customer']['User Type'].count()
	print("Subscriber: {}, Customer: {}, Filter: {}".format(count_subsc,count_custo,fl)) #to complet filter status
	
	# Display counts of gender if exist
	if city == "chicago" or city == "new york":
		#print('Stats for "Gender" ...')
		count_male = df[df['Gender'] == 'Male']['Gender'].count()
		count_female = df[df['Gender'] == 'Female']['Gender'].count()
		print("Female: {}, Male: {}, Filter: {}".format(count_female,count_male,fl)) #to complet filter status

		# Display earliest, most recent, and most common year of birth
		#earliest
		earliest_by = df['Birth Year'].min()
		recent_by = df['Birth Year'].max()
		com_by = df['Birth Year'].mode()[0]
		print("Earlist Birth Year: {}, Most Recent Birth Year: {}, Common Birth Year: {}, Filter: {}".format(earliest_by, recent_by, com_by, fl))
	else :
		print("Washington has no Gender and Birth Year options")	

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)

	i = 0
	j = 5
	while True:
		view = input('\nWould you like to view indivudial trip data? Type "yes" or "no".\n')
		if view.lower() != 'yes':
			break
		print(df[i:j])
		i += 5 
		j += 5

while True:
	city, month, day, fl = get_filters()
	df = load_data(city, month, day, fl)
	time_stats(df)
	station_stats(df)
	trip_duration_stats(df)
	user_stats(df)
	#print(df)

	restart = input('\nWould you like to restart? Enter yes or no.\n')
	if restart.lower() != 'yes':
		break
