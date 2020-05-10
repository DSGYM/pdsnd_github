# -*- coding: utf-8 -*-
"""
Created on Wed May  6 18:31:27 2020

@author: Markus
"""
import pandas as pd
import time

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}

MONTHS = {
    "january": "1",
    "february": "2",
    "march": "3",
    "april": "4",
    "may": "5",
    "june": "6",
    "july": "7",
    "august": "8",
    "september": "9",
    "october": "10",
    "november": "11",
    "december": "12",
    "none": None,
}

MONTHS_REVERSE = {
    "1": "January",
    "2": "February",
    "3": "March",
    "4": "April",
    "5": "May",
    "6": "June",
    "7": "July",
    "8": "August",
    "9": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}


DAYS = {
    "sunday": "0",
    "monday": "1",
    "tuesday": "2",
    "wednesday": "3",
    "thursday": "4",
    "friday": "5",
    "saturday": "6",
    "none": None,
}

DAYS_REVERSE = {
    "0": "Sunday",
    "1": "Monday",
    "2": "Tuesday",
    "3": "Wednesday",
    "4": "Thursday",
    "5": "Friday",
    "6": "Saturday",
}


def get_filters():
    dataset_found = False
    month_found = False
    day_found = False

    print("Hello! Let´s explorer some US Bikeshare data!")

    while dataset_found == False:
        dataset = (
            input(
                "Which city are you interested in? Washington, Chicago or New York City? "
            )
            .lower()
            .strip()
        )
        if dataset in CITY_DATA.keys():
            dataset_found = True
            dataset_var = CITY_DATA.get(dataset)
        else:
            print("Sorry, city was not found. Please check your spellings")

    while month_found == False:
        month = (
            input(
                "Which month are you interested in? Type 'None' if you do not want to apply a filter "
            )
            .lower()
            .strip()
        )
        if month in MONTHS.keys():
            month_found = True
            month_var = MONTHS.get(month)
        else:
            print("Please enter a valid month!")

    while day_found == False:
        day = (
            input(
                "Which weekday are you interested in? Type 'None' if you do not want to apply a filter "
            )
            .lower()
            .strip()
        )
        if day in DAYS.keys():
            day_found = True
            day_var = DAYS.get(day)
        else:
            print("Please enter a valid day!")
    return [dataset_var, month_var, day_var]


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
    df = None  # reference error before assignment otherwise

    try:
        df = pd.read_csv(f"data/{city}")
    except:
        print(f"Dataset for {city} not available")

    df["Start Time"] = pd.to_datetime(df["Start Time"], format="%Y-%m-%d %H:%M:%S")
    df["End Time"] = pd.to_datetime(df["End Time"], format="%Y-%m-%d %H:%M:%S")
    df["Month"] = df["Start Time"].dt.month
    df["Weekday"] = df["Start Time"].dt.weekday
    df["Hour"] = df["Start Time"].dt.hour
    if month is not None:
        df = df.query(f"Month == {month}")

    if day is not None:
        df = df.query(f"Weekday == {day}")

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # TO DO: display the most common month
    if month is not None:
        print(
            f'The most common month is: {MONTHS_REVERSE.get(str(df["Month"].mode()[0]))}'
        )
    else:
        print(
            "Statics for month is only available if dataset was not filtered by month."
        )

    # TO DO: display the most common day of week
    if day is not None:
        print(
            f'The most common weekday is: {DAYS_REVERSE.get(str(df["Weekday"].mode()[0]))}'
        )
    else:
        print("Statics for day is only available if dataset was not filtered by day.")

    # TO DO: display the most common start hour
    print(f'The most common hour is: {df["Hour"].mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # TO DO: display most commonly used start station
    start = (
        df.groupby(["Start Station"])
        .size()
        .reset_index(name="counts")
        .sort_values(by="counts", ascending=False)
    )
    print(
        f"Most popular start station is {start.iloc[0, 0]} with a count of {start.iloc[0, 1]}"
    )

    # TO DO: display most commonly used end station
    end = (
        df.groupby(["End Station"])
        .size()
        .reset_index(name="counts")
        .sort_values(by="counts", ascending=False)
    )
    print(
        f"Most popular end station is {end.iloc[0, 0]} with a count of {end.iloc[0, 1]}"
    )

    # TO DO: display most frequent combination of start station and end station trip
    combination = (
        df.groupby(["Start Station", "End Station"])
        .size()
        .reset_index(name="counts")
        .sort_values(by="counts", ascending=False)
    )
    print(
        f"Most popular combination are: {combination.iloc[0, 0]} as start station and {combination.iloc[0, 1]} as end station with a count of {combination.iloc[0, 2]}"
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # TO DO: display total travel time
    sum_travel_time = round(df["Trip Duration"].sum(), 2)

    # TO DO: display mean travel time
    mean_travel_time = round(df["Trip Duration"].mean(), 2)

    print(
        f"The overall travel time is {round(sum_travel_time / 60,0)} minutes with an avergage of {round(mean_travel_time / 60, 2)} minutes"
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # TO DO: Display counts of user types
    result = (
        df.groupby(["User Type"])
        .size()
        .reset_index(name="counts")
        .sort_values(by="counts", ascending=False)
    )
    print(
        f"{result.iloc[0,1]} customers were of type {str(result.iloc[0,0]).lower()}, {result.iloc[1,1]} customers were of type {str(result.iloc[1,0]).lower()}."
    )

    if city != "washington.csv":
        # TO DO: Display counts of gender
        result = (
            df.groupby(["Gender"])
            .size()
            .reset_index(name="counts")
            .sort_values(by="counts", ascending=False)
        )
        print(
            f"{result.iloc[0,1]} customers were {str(result.iloc[0,0]).lower()}, {result.iloc[1,1]} customers were {str(result.iloc[1,0]).lower()}."
        )

        # TO DO: Display earliest, most recent, and most common year of birth
        mostcommon = (
            df.groupby(["Birth Year"])
            .size()
            .reset_index(name="counts")
            .sort_values(by="counts", ascending=False)
        )
        earlierst = int(df["Birth Year"].min())
        recent = int(df["Birth Year"].max())

        print(
            f"The earlierst year of birth is {earlierst}, the most recent is {recent} and the most common is {int(mostcommon.iloc[0, 0])}"
        )
    else:
        print("No age and gender statistics available for washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.shape[0] > 0:
            five_lines = input(
                "Would you like to see the first 5 lines of the raw data? Yes or no?"
            )
            if five_lines.lower() == "yes":
                print(df.head(5))

            time_stats(df, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
        else:
            print(
                "No data available for the selected filter options. Please select other filters!"
            )

        restart = input("Would you like to restart? Enter yes or no.")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
