# From: http://espn.go.com/nfl/schedule

from datetime import datetime
from django.utils import timezone
from bs4 import BeautifulSoup
import urllib.request
import pytz
from django.core.management.base import NoArgsCommand

from footballseason.models import Game, Team, Pick, Record
import espn_common

#Call from CLI via: $ python manage.py generate_schedule

class Command(NoArgsCommand):

    season = 2017
    week_list = range(1,18)

    def add_games_from_one_week(self, season, week):
        url = "http://espn.go.com/nfl/schedule/_/year/{0}/week/{1}".format(season, week)
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

    def add_all_games(self):
        for week in self.week_list:
            print("Processing week {0}".format(week))
            self.add_games_from_one_week(self.season, week)

    def handle_noargs(self, **options):
        self.add_all_games()


    if __name__ == "__main__":
        main()
