from datetime import timezone

from django.contrib.auth.models import User
from django.db import models

import pytz


class Team(models.Model):
    team_name = models.CharField(max_length=200)
    wins = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    logo_name = models.CharField(max_length=1024)

    def record(self):
        if self.ties == 0:
            recordstr = "({0}-{1})".format(self.wins, self.loses)
        else:
            recordstr = "({0}-{1}-{2})".format(self.wins, self.loses, self.ties)
        return recordstr

    def __str__(self):
        return self.team_name


class Game(models.Model):
    season = models.IntegerField(default=0)
    week = models.IntegerField(default=0)
    home_team = models.ForeignKey(Team, related_name="game_home_team", on_delete=models.PROTECT)
    away_team = models.ForeignKey(Team, related_name="game_away_team", on_delete=models.PROTECT)
    game_time = models.DateTimeField("Game time")

    def gametime(self):
        try:
            # Season 2015 was different
            if self.season == 2015:
                # Week two was entered manually and has to be treated differently
                if self.week <= 2:
                    gametimestr = (
                        self.game_time.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%b %d, %I:%M %p")
                    )
                else:
                    gametimestr = self.game_time.strftime("%b %d, %I:%M %p")
            # All other seasons were entered as UTC time
            else:
                # Defaulting to central for now
                central_tz = pytz.timezone("America/Chicago")
                gametime_central = central_tz.normalize(self.game_time.astimezone(central_tz))
                gametimestr = gametime_central.strftime("%b %d, %I:%M %p")

        except NameError:
            gametimestr = ""
        return gametimestr

    def __str__(self):
        return "Week %d: %s at %s" % (self.week, self.away_team, self.home_team)


class Pick(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, related_name="picks", on_delete=models.PROTECT)
    team_to_win = models.ForeignKey(Team, on_delete=models.PROTECT)
    date_submitted = models.DateTimeField("Date pick was submitted", auto_now_add=True)

    def __str__(self):
        return "%s picks %s to win" % (self.user.first_name, self.team_to_win)


class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    season = models.IntegerField(default=0)
    week = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)

    def __str__(self):
        return "%s has %d wins in week %d of the %d season" % (self.user.first_name, self.wins, self.week, self.season)
