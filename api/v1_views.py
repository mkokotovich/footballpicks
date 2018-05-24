from rest_framework import viewsets
from rest_framework import permissions

from footballseason.models import Game, Team, Pick, Record
from api.serializers import GameSerializer, TeamSerializer, PickSerializer, RecordSerializer
from api.pagination import APIPagination
from api.permissions import IsAdminUserOrReadOnly


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    pagination_class = APIPagination
    filter_fields = ('home_team', 'away_team', 'season', 'week')
    ordering = "game_time"
    permission_classes = (IsAdminUserOrReadOnly,)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_fields = ('team_name',)
    ordering = "team_name"
    permission_classes = (IsAdminUserOrReadOnly,)


class PickViewSet(viewsets.ModelViewSet):
    queryset = Pick.objects.all()
    serializer_class = PickSerializer
    pagination_class = APIPagination
    filter_fields = ('user_name', 'game', 'team_to_win')
    ordering = "-id"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            # check if many is required
            if isinstance(data, list):
                kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    pagination_class = APIPagination
    filter_fields = ('user_name', 'season', 'week')
    ordering = "-id"
    permission_classes = (IsAdminUserOrReadOnly,)
