from django import forms

current_season=2016
season_choices = [(i,i) for i in range(2015,current_season+1)]

class SeasonChoice(forms.Form):
    season = forms.ChoiceField(choices=season_choices)
