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
from datetime import datetime
from math import ceil
from bs4 import BeautifulSoup
import urllib.request
import operator

from .models import Game, Team, Pick, Record

# constant - the start of "week 1", the tuesday before the first game
week1_start = datetime(2015,9,8,0,0,0)

def get_season():
    return int(2015)

def get_week():
    tdelta = datetime.now() - week1_start
    return int(ceil((tdelta.total_seconds()/(60*60*24))/7))

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
            record = Record.objects.get(user_name=pick.user_name, season=2015, week=last_game_week)
        except:
            record = Record(user_name=pick.user_name, season=2015, week=last_game_week, wins=0);
        record.wins += 1
        record.save()

def index(request):
    context = { 'current_week': get_week()}
    return render(request, 'footballseason/index.html', context)

def display(request, week_id):
    games_list = Game.objects.order_by('game_time').filter(week=week_id)
    context = { 'games_list': games_list , 'week_id': week_id}
    return render(request, 'footballseason/display.html', context)

@login_required(login_url='/login/')
def submit(request, week_id):
    games_list = Game.objects.order_by('game_time').filter(week=week_id)
    context = { 'games_list': games_list, 'week_id': week_id}
    return render(request, 'footballseason/submit.html', context)

def vote(request, week_id):
    games_list = Game.objects.order_by('game_time').filter(week=week_id)
    name=request.user.first_name
    # Game times were entered with a local timezone
    date_submitted = timezone.localtime(timezone.now())
    successful_submissions = 0
    for index, game in enumerate(games_list):
        try:
            selected_team_id=int(request.POST["game%d" % (index+1)])
        except:
            selected_team_id=0

        if (selected_team_id == game.away_team.id):
            # Away team chosen
            team_selected = game.away_team
        elif (selected_team_id == game.home_team.id):
            # Home team chosen
            team_selected = game.home_team
        elif (selected_team_id != 0):
            # Error!
            print("Error: Invalid selected_team_id: %d" % selected_team_id)
            return HttpResponseRedirect(reverse('footballseason:display', args=(week_id,)))

        if (selected_team_id != 0):
            # Check for an illegal pick
            if (game.game_time < date_submitted):
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
    return HttpResponseRedirect(reverse('footballseason:display', args=(week_id,)))

def update(request):
    url = "http://www.usatoday.com/sports/nfl/standings/"
    with urllib.request.urlopen(url) as response:
        html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    failure = 0

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
        infomsg = "Successfully updated standings"
        print(infomsg)
        messages.success(request, infomsg)

    context = { 'current_week': get_week()}
    return render(request, 'footballseason/index.html', context)

def records_default(request):
    return records_by_week(request, get_season(), get_week())

def records_by_week(request, season, week):
    record_list = Record.objects.filter(season=season, week=week).order_by('-wins')
    context = {'record_list': record_list, 'season': season, 'week': week }
    return render(request, 'footballseason/records.html', context)

def records_by_season(request, season):
    aggregate_dict = {}
    all_users = User.objects.all()
    for each_user in all_users:
        if (each_user.username == 'admin'):
            continue
        win_sum = sum([i.wins for i in Record.objects.filter(season=season, user_name=each_user.first_name)])
        aggregate_dict[each_user.first_name] = win_sum
    season_totals = sorted(aggregate_dict.items(), key=operator.itemgetter(1), reverse=True)
    context = {'season_totals': season_totals, 'season': season}
    return render(request, 'footballseason/records.html', context)
