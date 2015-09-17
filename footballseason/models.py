from django.db import models

class Team(models.Model):
	team_name = models.CharField(max_length=200)
	wins = models.IntegerField(default=0)
	loses = models.IntegerField(default=0)
	ties = models.IntegerField(default=0)

	def __str__(self):
		return self.team_name

class Game(models.Model):
	week = models.IntegerField(default=0)
	home_team = models.ForeignKey(Team, related_name='game_home_team')
	away_team = models.ForeignKey(Team, related_name='game_away_team')
	game_time = models.DateTimeField('Game time')

	def __str__(self):
		return "wk %d: %s at %s" % (self.week, self.away_team, self.home_team)

class Pick(models.Model):
	user_name = models.CharField(max_length=200)
	game = models.ForeignKey(Game)
	team_to_win = models.ForeignKey(Team)
	date_submitted = models.DateTimeField('Date pick was submitted')

	def __str__(self):
		return "%s picks %s to win" % (self.user_name, self.team_to_win)
