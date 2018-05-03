# This is not yet implemented
import logging

from datetime import datetime
from django.utils import timezone
from bs4 import BeautifulSoup
import urllib.request
import pytz
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from footballseason.models import Game, Team, Pick, Record
from footballseason.management.commands import cbs_common
from footballseason import fb_utils


LOG = logging.getLogger(__name__)

#Call from CLI via: $ python manage.py update_records

class Command(BaseCommand):


    def get_last_game_for_team(self, team):
        games = Game.objects.filter(Q(game_time__lte=timezone.now()) & Q(Q(home_team=team) | Q(away_team=team))).order_by('-game_time')
        if (len(games) == 0):
            LOG.error(f"Error: unable to find last game for team {team}")
            return None
        last_game = games[0]
        return last_game


    def update_user_records(self, team):
        try:
            last_game = self.get_last_game_for_team(team)
            last_game_week = last_game.week
        except Exception as ex:
            LOG.error(f"Error: Unable to find game to update records. Team: {team}, {ex}")
            return

        LOG.info(f"Updating winners for {last_game}")
        winning_picks = last_game.pick_set.filter(team_to_win=team)
        for pick in winning_picks:
            try:
                record = Record.objects.get(user_name=pick.user_name, season=fb_utils.get_season(), week=last_game_week)
            except:
                record = Record(user_name=pick.user_name, season=fb_utils.get_season(), week=last_game_week, wins=0);
            record.wins += 1
            LOG.info(f"Adding a win to {pick.user_name} for picking {team}")
            record.save()


    def update_records(self):
        url = "https://www.cbssports.com/nfl/standings"

        with urllib.request.urlopen(url) as response:
            html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        row1=soup.find_all('tr', {"class": "row1"})
        row2=soup.find_all('tr', {"class": "row2"})
        all_results = row1+row2
        successful_updates = 0
        for row in all_results:
            #import pdb
            #pdb.set_trace()
            # Each row is one team's record
            entries=row.find_all('td')
            # it goes name, W, L, T
            cbs_team_name = entries[0].a.text
            team_name = cbs_common.cbs_team_names[cbs_team_name]
            wins = int(entries[1].text)
            loses = int(entries[2].text)
            ties = int(entries[3].text)

            try:
                team = Team.objects.get(team_name=team_name)
                # An existing team was found, update standings
                if (team.wins != wins or team.loses != loses or team.ties != ties):
                    LOG.info(f"{team_name} needs updating")
                    successful_updates += 1

                if (team.wins < wins):
                    # This team won, update records. Assuming we update at least once a week
                    self.update_user_records(team)

                team.wins=wins
                team.loses=loses
                team.ties=ties
                team.save()
            except ObjectDoesNotExist:
                # Could not find team, this shouldn't happen
                LOG.error(f"Could not find team {team_name}, could not update standings")
        LOG.info(f"Successfully updated {successful_updates} teams")


    def handle(self, *args, **options):
        self.update_records()


    if __name__ == "__main__":
        cmd = Command()
        cmd.update_records()
