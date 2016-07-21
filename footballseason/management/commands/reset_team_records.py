from django.core.management.base import NoArgsCommand
from footballseason.models import Game, Team, Pick, Record

#Call from CLI via: $ python manage.py reset_team_records

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        self.reset_all_team_records()

    def reset_all_team_records(self):
        for team in Team.objects.all():
            print("Resetting wins and losses for {0}".format(team.team_name))
            team.wins=0
            team.loses=0
            team.ties=0
            team.save()
