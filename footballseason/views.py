from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Game, Team, Pick

def index(request):
	context = { }
	return render(request, 'footballseason/index.html', context)

def display(request, week_id):
	games_list = Game.objects.order_by('game_time').filter(week=week_id)
	context = { 'games_list': games_list , 'week_id': week_id}
	return render(request, 'footballseason/display.html', context)

def submit(request, week_id):
	games_list = Game.objects.order_by('game_time').filter(week=week_id)
	context = { 'games_list': games_list, 'week_id': week_id}
	return render(request, 'footballseason/submit.html', context)

def vote(request, week_id):
	games_list = Game.objects.order_by('game_time').filter(week=week_id)
	name=request.POST["user"]
	for index, game in enumerate(games_list):
		selected_team_id=int(request.POST["game%d" % (index+1)])
		if (selected_team_id == game.away_team.id):
			# Away team won, create pick and add game to it
			pick = Pick(user_name=name, game=game, team_to_win=game.away_team, date_submitted=timezone.now())
			pick.save()
		elif (selected_team_id == game.home_team.id):
			# Home team won, create pick and add game to it
			pick = Pick(user_name=name, game=game, team_to_win=game.home_team, date_submitted=timezone.now())
			pick.save()
		else:
			# Error!
			print("Error: Invalid selected_team_id: %d" % selected_team_id)


	# Always return an HttpResponseRedirect after successfully dealing
	# with POST data. This prevents data from being posted twice if a
	# user hits the Back button.
	return HttpResponseRedirect(reverse('footballseason:display', args=(week_id,)))

