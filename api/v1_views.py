import logging

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from footballseason.models import Game, Team, Pick, Record
from api.serializers import GameSerializer, TeamSerializer, PickSerializer, RecordSerializer
from api.pagination import APIPagination
from api.permissions import IsAdminUserOrReadOnly
import footballseason.fb_utils as utils
from footballseason.espn_api import espn_api_v3


LOG = logging.getLogger(__name__)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    pagination_class = APIPagination
    filter_fields = ('home_team', 'away_team', 'season', 'week')
    ordering = "game_time"
    permission_classes = (IsAdminUserOrReadOnly,)

    def find_game_id(self, games, away_team, home_team):
        for game in games:
            if away_team in game.away_team.team_name and home_team in game.home_team.team_name:
                return game.id
        LOG.error(f"No game found for {away_team} vs {home_team}")
        return 0

    @action(detail=False)
    def scores(self, request):
        try:
            scores = espn_api_v3.get_scores(espn_api_v3.NFL)
        except Exception:
            LOG.exception("Unable to retrieve scores")
            raise APIException("Unable to retrieve scores")
        # Mock scores
        # scores = {index: ['home', '0', 'away', '7', '0:15 in 4th'] for index in range(0, 16)}

        LOG.info(f"Retrieved {len(scores)} games from espn api")

        current_season = utils.get_season()
        current_week = utils.get_week()
        games = Game.objects.order_by('game_time').filter(season=current_season, week=current_week)

        score_list = [
            {
                "game_id": self.find_game_id(games=games, home_team=score[0], away_team=score[2]),
                "away_score": score[1],
                "home_score": score[3],
                "time": score[4],
            } for score in scores.values()
        ]

        return Response(score_list)


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
