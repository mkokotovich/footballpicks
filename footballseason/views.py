from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from math import ceil

from .models import Game, Team, Pick

# constant - the start of "week 1", the tuesday before the first game
week1_start = datetime(2015,9,8,0,0,0)

def get_week():
    tdelta = datetime.now() - week1_start
    return int(ceil((tdelta.total_seconds()/(60*60*24))/7))

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
            # A team was selected, first look to see if a pick already exists
            try:
                pick = game.pick_set.get(user_name=name)
                # An existing pick was found, update selection
                pick.team_to_win=team_selected
                pick.date_submitted=timezone.now()
            except ObjectDoesNotExist:
                # No existing pick found, create new pick
                pick = Pick(user_name=name, game=game, team_to_win=team_selected, date_submitted=timezone.now())

            pick.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('footballseason:display', args=(week_id,)))

