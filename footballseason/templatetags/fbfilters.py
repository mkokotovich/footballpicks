from django.template import Library
from footballseason.models import Team, Game

register = Library()


@register.filter
def display_record(team):
    return team.record()


@register.filter
def display_gametime(game):
    return game.gametime()
