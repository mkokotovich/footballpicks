from django.contrib import admin

from .models import Team, Game, Pick, Record

class TeamAdmin(admin.ModelAdmin):
    fields = ['team_name', 'wins', 'loses', 'ties']
class GameAdmin(admin.ModelAdmin):
    fields = ['season', 'week', 'away_team', 'home_team', 'game_time']
class PickAdmin(admin.ModelAdmin):
    fields = ['user', 'game', 'team_to_win', 'date_submitted']
class RecordAdmin(admin.ModelAdmin):
    fields = ['user', 'season', 'week', 'wins']

admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Pick, PickAdmin)
admin.site.register(Record, RecordAdmin)
