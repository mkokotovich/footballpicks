import logging
from django.core.management.base import BaseCommand
from footballseason.models import Team


LOG = logging.getLogger(__name__)


# Call from CLI via: $ python manage.py reset_team_records
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.reset_all_team_records()

    def reset_all_team_records(self):
        for team in Team.objects.all():
            LOG.info("Resetting wins and losses for {0}".format(team.team_name))
            team.wins = 0
            team.loses = 0
            team.ties = 0
            team.save()
