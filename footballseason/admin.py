from django.contrib import admin

from .models import Team, Game, Pick

class TeamAdmin(admin.ModelAdmin):
	fields = ['team_name', 'wins', 'loses', 'ties']
class GameAdmin(admin.ModelAdmin):
	fields = ['week', 'away_team', 'home_team', 'game_time']
class PickAdmin(admin.ModelAdmin):
	fields = ['user_name', 'game', 'team_to_win', 'date_submitted']

admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Pick, PickAdmin)
