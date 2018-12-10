import logging
import urllib.request

from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from bs4 import BeautifulSoup

from footballseason.models import Game, Team, Record
from footballseason.management.commands import cbs_common
from footballseason import fb_utils


LOG = logging.getLogger(__name__)


# Call from CLI via: $ python manage.py update_records
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
        winning_picks = last_game.picks.filter(team_to_win=team)
        for pick in winning_picks:
            try:
                record = Record.objects.get(user=pick.user, season=fb_utils.get_season(), week=last_game_week)
            except Record.DoesNotExist:
                record = Record(user=pick.user, season=fb_utils.get_season(), week=last_game_week, wins=0)
            record.wins += 1
            LOG.info(f"Adding a win to {pick.user.first_name} for picking {team}")
            record.save()

    def update_records(self):
        url = "https://www.cbssports.com/nfl/standings"

        with urllib.request.urlopen(url) as response:
            html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        all_results = soup.find_all('tr', {"class": "TableBase-bodyTr"})
        successful_updates = 0
        for row in all_results:
            # Each row is one team's record
            entries = row.find_all('td')
            # it goes name, W, L, T
            cbs_team_name_raw = entries[0].text.strip()
            # Remove playoff indicators (e.g.  - x)
            cbs_team_name = cbs_team_name_raw.split(' - ')[0]
            team_name = cbs_common.cbs_team_names[cbs_team_name]
            wins = int(entries[1].text.strip())
            loses = int(entries[2].text.strip())
            ties = int(entries[3].text.strip())

            try:
                team = Team.objects.get(team_name=team_name)
                # An existing team was found, update standings
                if (team.wins != wins or team.loses != loses or team.ties != ties):
                    LOG.info(f"{team_name} needs updating")
                    successful_updates += 1

                if (team.wins < wins):
                    # This team won, update records. Assuming we update at least once a week
                    self.update_user_records(team)

                team.wins = wins
                team.loses = loses
                team.ties = ties
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
