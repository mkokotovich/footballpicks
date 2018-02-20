from django import forms
from footballseason import fb_utils

current_season=fb_utils.get_season()
season_choices = [(i,i) for i in range(2015,current_season+1)]

class SeasonChoice(forms.Form):
    season = forms.ChoiceField(choices=season_choices)
