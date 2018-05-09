from rest_framework import viewsets
from footballseason.models import Game, Team, Pick, Record
from api.serializers import GameSerializer, TeamSerializer, PickSerializer, RecordSerializer
from api.pagination import APIPagination


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    pagination_class = APIPagination
    filter_fields = ('home_team', 'away_team', 'season', 'week')
    ordering = "-game_time"


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_fields = ('team_name',)
    ordering = "team_name"


class PickViewSet(viewsets.ModelViewSet):
    queryset = Pick.objects.all()
    serializer_class = PickSerializer
    pagination_class = APIPagination
    filter_fields = ('user_name', 'game', 'team_to_win')
    ordering = "-id"


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    pagination_class = APIPagination
    filter_fields = ('user_name', 'season', 'week')
    ordering = "-id"
