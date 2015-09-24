from django.db import models
from datetime import timezone

class Team(models.Model):
    team_name = models.CharField(max_length=200)
    wins = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)

    def record(self):
        if (self.ties == 0):
            recordstr = "({0}-{1})".format(self.wins, self.loses)
        else:
            recordstr = "({0}-{1}-{2})".format(self.wins, self.loses, self.ties)
        return recordstr

    def __str__(self):
        return self.team_name

class Game(models.Model):
    week = models.IntegerField(default=0)
    home_team = models.ForeignKey(Team, related_name='game_home_team')
    away_team = models.ForeignKey(Team, related_name='game_away_team')
    game_time = models.DateTimeField('Game time')

    def gametime(self):
        try:
            gametimestr = self.game_time.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%b %d, %I:%M %p") 
        except NameError:
            gametimestr = ""
        return gametimestr

    def __str__(self):
        return "Week %d: %s at %s" % (self.week, self.away_team, self.home_team)

class Pick(models.Model):
    user_name = models.CharField(max_length=200)
    game = models.ForeignKey(Game)
    team_to_win = models.ForeignKey(Team)
    date_submitted = models.DateTimeField('Date pick was submitted')

    def __str__(self):
        return "%s picks %s to win" % (self.user_name, self.team_to_win)

class Record(models.Model):
    user_name = models.CharField(max_length=200)
    season = models.IntegerField(default=0)
    week = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)

    def __str__(self):
        return "%s has %d wins in week %d of the %d season" % (self.user_name, self.wins, self.week, self.season)
