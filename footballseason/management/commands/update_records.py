# This is not yet implemented

from datetime import datetime
from django.utils import timezone
from bs4 import BeautifulSoup
import urllib.request
import pytz
from django.core.management.base import NoArgsCommand

from footballseason.models import Game, Team, Pick, Record
from footballseason.management.commands import espn_common
from footballseason import fb_utils

#Call from CLI via: $ python manage.py update_records

class Command(NoArgsCommand):

    season = fb_utils.get_season()

    def add_games_from_one_week(self, season, week):
        url = "http://www.espn.com/nfl/standings/_/season/{}/group/league".format(season)
        print("url: {0}".format(url))

        with urllib.request.urlopen(url) as response:
            html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        # Each table is a day (e.g. Thursday, Sunday, Monday)
        for table in soup.findAll("table", class_="schedule"):
            odd=table.find_all('tr', {"class": "odd"})
            even=table.find_all('tr', {"class": "even"})
            all_results = odd+even
            for row in all_results:
                # Each row is one game
                game_time_data = row.find('td', { "data-behavior":"date_time" } )
                if game_time_data == None:
                    # bye teams
                    continue
                game_time = game_time_data['data-date']
                #  2016-12-16T01:25Z
                game_datetime = datetime.strptime(game_time, "%Y-%m-%dT%H:%MZ")
                game_tzaware = pytz.utc.localize(game_datetime)
                current_tz = timezone.get_current_timezone()
                local_gametime = current_tz.normalize(game_tzaware.astimezone(current_tz))
                print(timezone.is_aware(local_gametime))
                team_names = []
                for team_abbr in row.find_all('abbr'):
                    team_names.append(espn_common.espn_team_names[team_abbr.contents[0].lower()])
                try:
                    away = Team.objects.get(team_name=team_names[0])
                    home = Team.objects.get(team_name=team_names[1])
                except ObjectDoesNotExist:
                    # Could not find team, this shouldn't happen
                    print("Count not find either team {0} or {1}, unable to add game to schedule".format(team_names[0], team_names[1]))
                    continue
                newgame = Game(season=season, week=week, home_team=home, away_team=away, game_time=game_tzaware)
                print("Adding: {0}".format(newgame))
                newgame.save()

    def update_records_for_current_week(self):
        season = fb_utils.get_season()
        week = fb_utils.get_week()
        print("Updating records for season {} week {}".format(season, week))
        self.update_records_for_week(season, week)

    def handle_noargs(self, **options):
        self.update_records_for_current_week()


    if __name__ == "__main__":
        cmd = Command()
        cmd.update_records_for_current_week()
