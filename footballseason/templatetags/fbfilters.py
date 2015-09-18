from django.template import Library
from footballseason.models import Team

register = Library()

@register.filter
def display_record( team ):
  return team.record()
