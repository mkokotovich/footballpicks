from datetime import datetime, timedelta
from math import ceil

def get_week1_start():
    current_season = get_season()
    return get_week1_start_for_season(current_season)

# the start of "week 1", the tuesday before the first game
# Not sure of a prettier way to do this
# Week 1 start should be the Tuesday after Labor Day
def get_week1_start_for_season(season):
    if (season == 2015):
        week1_start = datetime(2015,9,8,0,0,0)
    elif (season == 2016):
        week1_start = datetime(2016,9,6,0,0,0)
    elif (season == 2017):
        week1_start = datetime(2017,9,5,0,0,0)
    elif (season == 2018):
        week1_start = datetime(2018,9,4,0,0,0)
    elif (season == 2019):
        week1_start = datetime(2019,9,3,0,0,0)
    elif (season == 2020):
        week1_start = datetime(2020,9,7,0,0,0)
    elif (season == 2021):
        week1_start = datetime(2021,9,6,0,0,0)
    elif (season == 2022):
        week1_start = datetime(2022,9,5,0,0,0)
    elif (season == 2023):
        week1_start = datetime(2023,9,3,0,0,0)
    else:
        week1_start = datetime(2015,9,8,0,0,0)
    return week1_start

def get_gameday_for_season_and_week(season, week):
    week1_start = get_week1_start_for_season(season)
    return week1_start + timedelta(days=5) + timedelta(days=(7*(week-1)))

def get_month_for_week(season, week):
    week_gameday = get_gameday_for_season_and_week(season, week)
    return week_gameday.month

def get_first_and_last_weeks_for_a_month(season, month):
    gameday = get_gameday_for_season_and_week(season, 1)
    first_week = 0
    last_week = 0
    num_weeks = 1
    # Find first week of month
    while gameday.month != month:
        gameday += timedelta(days=(7))
        num_weeks += 1
    first_week = num_weeks
    # Find last week of month
    last_gameday = gameday
    while gameday.month == month and num_weeks < 18:
        gameday += timedelta(days=(7))
        num_weeks += 1
    last_week = num_weeks - 1
    return (first_week, last_week)

def get_season():
    now = datetime.now()
    if (now.month > 1):
        return now.year
    else:
        # Jan and Feb should be in the year prior, to stick to seasons
        return now.year - 1

def get_week():
    now = datetime.now()
    week1_start = get_week1_start()
    if (now < week1_start):
        return 1
    tdelta = now - week1_start
    week = int(ceil((tdelta.total_seconds()/(60*60*24))/7))
    if (week > 17):
        week = 17
    return week

