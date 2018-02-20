from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, timedelta
import calendar
from bs4 import BeautifulSoup
import urllib.request
import operator
from footballseason.espn_api import espn_api_v3

from .models import Game, Team, Pick, Record
from .forms import SeasonChoice
import footballseason.fb_utils as utils


def get_last_game_for_team(team):
    games = Game.objects.filter(Q(game_time__lte=timezone.now()) & Q(Q(home_team=team) | Q(away_team=team))).order_by('-game_time')
    if (len(games) == 0):
        print("Error: unable to find last game for team {0}".format(team))
        return None
    last_game = games[0]
    return last_game

def update_records(team):
    try:
        last_game = get_last_game_for_team(team)
        last_game_week = last_game.week
    except:
        # Error
        print("Error: Unable to find game to update records. Team: {0}".format(team))
        return 0

    winning_picks = last_game.pick_set.filter(team_to_win=team)
    for pick in winning_picks:
        try:
            record = Record.objects.get(user_name=pick.user_name, season=utils.get_season(), week=last_game_week)
        except:
            record = Record(user_name=pick.user_name, season=utils.get_season(), week=last_game_week, wins=0);
        record.wins += 1
        record.save()

def index(request):
    season_id = 0
    if request.method == 'POST':
        season_choice = SeasonChoice(request.POST)
        if season_choice.is_valid():
            season_id = season_choice.cleaned_data['season']
    if (season_id == 0):
        season_id = utils.get_season()
    season_choice = SeasonChoice(initial={'season':season_id})
    week_id = utils.get_week()
    if (season_id != utils.get_season()):
        # If this is a past season, set the week to week 18
        week_id = 18
    context = { 'season_id': season_id,
                'week_id': week_id,
                'season_choice': season_choice}
    return render(request, 'footballseason/index.html', context)

def display(request, season_id, week_id):
    season_id = int(season_id)
    week_id = int(week_id)
    if request.method == 'POST':
        season_choice = SeasonChoice(request.POST)
        if season_choice.is_valid():
            season_id = season_choice.cleaned_data['season']
    if (season_id == 0):
        season_id = utils.get_season()
    season_choice = SeasonChoice(initial={'season':season_id})
    filter_season_id = season_id
    if (season_id == 2015):
        #First season (2015) didn't have season populated, it is stored as 0
        filter_season_id = 0
    if (week_id == 0):
        week_id = utils.get_week()
    games_list = Game.objects.order_by('game_time').filter(season=filter_season_id, week=week_id)
    context = { 'games_list': games_list ,
                'season_id': season_id,
                'week_id': week_id,
                'season_choice': season_choice}
    return render(request, 'footballseason/display.html', context)

@login_required(login_url='/login/')
def submit(request, season_id, week_id):
    season_id = int(season_id)
    week_id = int(week_id)
    if request.method == 'POST':
        season_choice = SeasonChoice(request.POST)
        if season_choice.is_valid():
            season_id = season_choice.cleaned_data['season']
    if (season_id == 0):
        season_id = utils.get_season()
    season_choice = SeasonChoice(initial={'season':season_id})
    filter_season_id = season_id
    if (season_id == 2015):
        #First season (2015) didn't have season populated, it is stored as 0
        filter_season_id = 0
    if (week_id == 0):
        week_id = utils.get_week()
    games_list = Game.objects.order_by('game_time').filter(season=filter_season_id, week=week_id)
    game_and_pick_list = []
    for game in games_list:
        side = ''
        try:
            pick = game.pick_set.get(user_name=request.user.first_name)
            if (pick.team_to_win == game.home_team):
                side = 'home'
            elif (pick.team_to_win == game.away_team):
                side = 'away'
        except ObjectDoesNotExist:
            pass

        game_and_pick_list.append((game, side))

    context = { 'game_and_pick_list': game_and_pick_list,
                'season_id': season_id,
                'week_id': week_id,
                'season_choice': season_choice}

    return render(request, 'footballseason/submit.html', context)

def pick_is_after_gametime(gametime, date_submitted):
    # TODO: This logic should hopefully go away with new season's games
    # Adjust for UTC issue (gametimes were added in the wrong timezone. Games
    # that are supposed to start at 7:25PM have a gametime of 2:25PM)
    adjusted_gametime = gametime + timedelta(hours=5)
    return (date_submitted > adjusted_gametime)

def vote(request, season_id, week_id):
    season_id = int(season_id)
    week_id = int(week_id)
    filter_season_id = season_id
    if (season_id == 2015):
        #First season (2015) didn't have season populated, it is stored as 0
        filter_season_id = 0
    games_list = Game.objects.order_by('game_time').filter(season=filter_season_id, week=week_id)
    name=request.user.first_name
    date_submitted = timezone.now()
    successful_submissions = 0
    for index, game in enumerate(games_list):
        try:
            selected_team_id=int(request.POST["game%d" % (index+1)])
        except:
            selected_team_id=0
            messages.warning(request, "No pick entered for {0}".format(game))

        if (selected_team_id == game.away_team.id):
            # Away team chosen
            team_selected = game.away_team
        elif (selected_team_id == game.home_team.id):
            # Home team chosen
            team_selected = game.home_team
        elif (selected_team_id != 0):
            # Error!
            print("Error: Invalid selected_team_id: %d" % selected_team_id)
            return HttpResponseRedirect(reverse('footballseason:display', args=(season_id,week_id,)))

        if (selected_team_id != 0):
            # Check for an illegal pick
            if (pick_is_after_gametime(game.game_time, date_submitted)):
                errormsg="Unable to submit pick for ({0}), game already started.".format(game)
                print(errormsg)
                messages.error(request, errormsg)
                continue

            # A team was selected, first look to see if a pick already exists
            try:
                pick = game.pick_set.get(user_name=name)
                # An existing pick was found, update selection
                pick.team_to_win=team_selected
                pick.date_submitted=date_submitted
            except ObjectDoesNotExist:
                # No existing pick found, create new pick
                pick = Pick(user_name=name, game=game, team_to_win=team_selected, date_submitted=date_submitted)

            pick.save()
            successful_submissions += 1

    if (successful_submissions > 0):
        infomsg = "Successfully submitted {0} picks for {1}".format(successful_submissions, request.user.first_name)
        print(infomsg)
        messages.success(request, infomsg)

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('footballseason:display', args=(season_id, week_id,)))

def update(request):
    url = "https://www.usatoday.com/sports/nfl/standings/"
    req = urllib.request.Request(url)
    req.add_header('Pragma', 'no-cache')
    req.add_header('Cache-Control', 'no-cache')
    response = urllib.request.urlopen(req)
    html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    failure = 0
    successful_updates = 0

    # For each division:
    for node in soup.find_all('table'):
        for row in node.find_all('tr'):
            teamname = row.find('th').text.strip()
            cols = row.find_all('td')
            if (len(cols) < 3):
                continue
            wins = int(cols[0].text)
            loses = int(cols[1].text)
            ties = int(cols[2].text)
            try:
                team = Team.objects.get(team_name=teamname)
                # An existing team was found, update standings
                if (team.wins != wins or team.loses != loses or team.ties != ties):
                    successful_updates += 1

                if (team.wins < wins):
                    # This team won, update records. Assuming we update at least once a week
                    update_records(team)
                team.wins=wins
                team.loses=loses
                team.ties=ties
                team.save()
            except ObjectDoesNotExist:
                # Could not find team, this shouldn't happen
                errormsg = "Could not find team {0}, could not update standings".format(teamname)
                print(errormsg)
                messages.error(request, errormsg)
                failure=1

    if (failure == 0):
        if (successful_updates > 0):
            infomsg = "Successfully updated standings for {0} teams".format(successful_updates)
            messages.success(request, infomsg)
        else:
            infomsg = "No updates available"
            messages.info(request, infomsg)
        print(infomsg)

    context = { 'season_id': utils.get_season(), 'week_id': utils.get_week()}
    return render(request, 'footballseason/index.html', context)

def records(request, season_id=0, week=0, view="week", month=0):
    season_id = int(season_id)
    week_id = int(week)
    month_id = int(month)
    if request.method == 'POST':
        season_choice = SeasonChoice(request.POST)
        if season_choice.is_valid():
            season_id = season_choice.cleaned_data['season']

    # If week isn't supplied, use the current week
    if (week_id == 0):
        week_id = utils.get_week()

    # If season isn't supplied, use the current season
    if (season_id == 0):
        season_id = utils.get_season()

    # Get the season choice for the context
    season_choice = SeasonChoice(initial={'season':utils.get_season() if view == "alltime" else season_id})

    # If the view is week, we don't need the extra stats, just return the basic count
    if view == "week":
        # Find the wins for the specified week
        record_list = Record.objects.filter(season=season_id, week=week_id).order_by('-wins')
        context = {'record_list': record_list,
                   'season_id': season_id,
                   'week': week_id,
                   'season_choice': season_choice}
        return render(request, 'footballseason/records.html', context)

    game_season = season_id
    if (season_id == 2015):
        # 2015 games didnt have a season populated
        game_season = 0

    aggregate_list = [] 
    all_users = User.objects.all()
    current_time = timezone.now()
    for each_user in all_users:
        if (each_user.username == 'admin'):
            continue
        # First find the number of wins from the Record table
        query = Record.objects.filter(user_name=each_user.first_name)
        # If we aren't doing an all-time view, filter by the current season
        if view != "alltime":
            query = query.filter(season=season_id)
        # If month view, filter by the weeks in that month
        if view == "month":
            first_week, last_week = utils.get_first_and_last_weeks_for_a_month(season_id, month_id)
            query = query.filter(week__gte=first_week, week__lte=last_week)
        win_sum = sum([i.wins for i in query])
        # Then find the total number of games from the Pick table
        query = Pick.objects.filter(game__game_time__lte=current_time, user_name=each_user.first_name)
        # If we aren't doing an all-time view, filter by the current season
        if view != "alltime":
            query = query.filter(game__season=game_season)
        # If month view, filter by the weeks in that month
        if view == "month":
            query = query.filter(game__game_time__month=month_id)
        total_games = query.count()
        if (total_games == 0):
            continue

        percentage = win_sum / total_games
        aggregate_list.append((each_user.first_name, win_sum, total_games - win_sum, percentage))
    season_totals = []
    if view == "month":
        # Sort by wins, not percentages
        season_totals = sorted(aggregate_list, key=lambda record: record[1], reverse=True)
    else:
        # Sort by percentage
        season_totals = sorted(aggregate_list, key=lambda record: record[3], reverse=True)
    context = {'season_totals': season_totals,
               'season_id': season_id,
               'season_choice': season_choice,
               'record_view': view}
    if view != "alltime":
        context['season_id'] = utils.get_season()
    if view == "month":
        context['month'] = calendar.month_name[month_id]
    return render(request, 'footballseason/records.html', context)

def live(request):
    season_id = utils.get_season()
    filter_season_id = season_id
    if (season_id == 2015):
        #First season (2015) didn't have season populated, it is stored as 0
        filter_season_id = 0
    week_id = utils.get_week()
    games_list = Game.objects.order_by('game_time').filter(season=filter_season_id, week=week_id)
    scores = espn_api_v3.get_scores(espn_api_v3.NFL)
    live_list = []
    # sort the scores in the order of our games
    for game in games_list:
        for score in scores.values():
            if (score[0] in game.away_team.team_name and score[2] in game.home_team.team_name):
                live_list.append((game, score))
        
    context = { 'live_list': live_list , 'season_id': season_id, 'week_id': week_id}
    return render(request, 'footballseason/live.html', context)

