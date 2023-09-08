from django.test import TestCase
from .models import Team, Game, Pick, Record


class TeamTests(TestCase):
    def test_record_with_tie(self):
        """
        Record output should include ties
        """
        team = Team(wins=1, loses=2, ties=3)
        self.assertEqual(team.record(), "(1-2-3)")

    def test_record_with_no_ties(self):
        """
        Record output should not include a spot for ties
        """
        team = Team(wins=1, loses=2, ties=0)
        self.assertEqual(team.record(), "(1-2)")
