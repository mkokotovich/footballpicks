# From: http://espn.go.com/nfl/schedule
import logging
import sys
import datetime
import urllib.request

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import ProtectedError
from bs4 import BeautifulSoup
import pytz

from footballseason.models import Game, Team
from footballseason import fb_utils
import footballseason.management.commands.espn_common as espn_common


LOG = logging.getLogger(__name__)


# Call from CLI via: $ python manage.py generate_schedule
class Command(BaseCommand):
    season = fb_utils.get_season()
    week_list = range(1, fb_utils.NUM_WEEKS + 1)

    def add_games_from_one_week(self, season, week):
        url = "http://espn.go.com/nfl/schedule/_/year/{0}/week/{1}".format(season, week)
        LOG.info("url: {0}".format(url))
        with urllib.request.urlopen(url) as response:
            html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        all_game_ids = []
        # Each div is a day (e.g. Thursday, Sunday, Monday)
        for div in soup.findAll("div", "ScheduleTables"):
            # Find the date of this day
            date_string = div.find("div", class_="Table__Title").getText().strip()
            LOG.info(f"found games on {date_string}")

            for table in div.findAll("table", class_="Table"):
                all_results = table.find_all("tr")
                for row in all_results:
                    # Each row is one game
                    game_time_data = row.find("td", class_="date__col")
                    if game_time_data is None:
                        # bye teams
                        continue
                    game_time = game_time_data.getText()
                    if game_time == "TBD":
                        # Just default to noon game for TBD games
                        game_time = "1:00 PM"
                    # "1:00 PM"
                    if game_time == "LIVE":
                        # Skip games that happen to be currently playing
                        continue
                    game_time_stamp = f"{game_time} {date_string}"
                    game_datetime = datetime.datetime.strptime(game_time_stamp, "%I:%M %p %A, %B %d, %Y")
                    # Times are in Eastern, adjust to Central
                    game_datetime = game_datetime - datetime.timedelta(hours=1)
                    # Make gametime timezone aware, times are retrieved in EST
                    game_datetime = pytz.timezone("US/Central").localize(game_datetime)

                    # find the team by using the link
                    links = [anchorlink["href"] for anchorlink in row.find_all(class_="AnchorLink")]
                    # '/nfl/team/_/name/no/new-orleans-saints'
                    away_abbr = links[0].split("/")[5]
                    away_name = espn_common.espn_team_names[away_abbr]
                    home_abbr = links[2].split("/")[5]
                    home_name = espn_common.espn_team_names[home_abbr]

                    try:
                        away = Team.objects.get(team_name=away_name)
                        home = Team.objects.get(team_name=home_name)
                    except ObjectDoesNotExist:
                        # Could not find team, this shouldn't happen
                        LOG.info(
                            f"Count not find either team {home_name} or {away_name}, unable to add game to schedule"
                        )
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
