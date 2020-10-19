# From: http://espn.go.com/nfl/schedule
import logging
import sys
import datetime
import urllib.request

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import ProtectedError
from bs4 import BeautifulSoup

from footballseason.models import Game, Team
from footballseason import fb_utils
import footballseason.management.commands.espn_common as espn_common


LOG = logging.getLogger(__name__)


# Call from CLI via: $ python manage.py generate_schedule
class Command(BaseCommand):

    season = fb_utils.get_season()
    week_list = range(1, 18)

    def add_games_from_one_week(self, season, week):
        url = "http://espn.go.com/nfl/schedule/_/year/{0}/week/{1}".format(season, week)
        LOG.info("url: {0}".format(url))
        with urllib.request.urlopen(url) as response:
            html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        all_game_ids = []
        # Each table is a day (e.g. Thursday, Sunday, Monday)
        for table in soup.findAll("table", class_="schedule"):
            odd = table.find_all('tr', {"class": "odd"})
            even = table.find_all('tr', {"class": "even"})
            all_results = odd + even
            for row in all_results:
                # Each row is one game
                game_time_data = row.find('td', {"data-behavior": "date_time"})
                if game_time_data is None:
                    # bye teams
                    continue
                game_time = game_time_data['data-date']
                # 2016-12-16T01:25Z
                game_datetime = datetime.datetime.strptime(game_time, "%Y-%m-%dT%H:%MZ")
                # Make gametime timezone aware
                game_datetime = game_datetime.replace(tzinfo=datetime.timezone.utc)

                team_names = []
                for team_abbr in row.find_all('abbr'):
                    team_names.append(espn_common.espn_team_names[team_abbr.contents[0].lower()])
                try:
                    away = Team.objects.get(team_name=team_names[0])
                    home = Team.objects.get(team_name=team_names[1])
                except ObjectDoesNotExist:
                    # Could not find team, this shouldn't happen
                    LOG.info("Count not find either team {0} or {1}, unable to add game to schedule".format(team_names[0], team_names[1]))
                    sys.exit(1)
                try:
                    obj = Game.objects.get(season=season, week=week, home_team=home, away_team=away)
                except Game.DoesNotExist:
                    obj = Game(season=season, week=week, home_team=home, away_team=away, game_time=game_datetime)
                    LOG.info("Adding: {0}".format(obj))
                else:
                    if obj.game_time != game_datetime:
                        obj.game_time = game_datetime
                        LOG.info(f"{obj} was already on the schedule, updating gametime and saving")
                finally:
                    obj.save()
                    all_game_ids.append(obj.id)

        removed_games = Game.objects.filter(season=season, week=week).exclude(id__in=all_game_ids)

        if removed_games:
            try:
                LOG.info(f"Removing {removed_games.count()} games: {list(removed_games)}")
                removed_games.delete()
            except ProtectedError:
                LOG.info("Unable to remove games with picks")

    def add_all_games(self):
        for week in self.week_list:
            LOG.info("Processing week {0}".format(week))
            self.add_games_from_one_week(self.season, week)

    def handle(self, *args, **options):
        self.add_all_games()
