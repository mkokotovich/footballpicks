import logging

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.utils import timezone
from django.contrib.auth.models import User

from footballseason.models import Game, Team, Pick, Record
from api.serializers import GameSerializer, TeamSerializer, PickSerializer
from api.pagination import APIPagination
from api.permissions import IsAdminUserOrReadOnly
import footballseason.fb_utils as utils
from footballseason.espn_api import espn_api_v3


LOG = logging.getLogger(__name__)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    pagination_class = APIPagination
    filterset_fields = ("home_team", "away_team", "season", "week")
    ordering = "game_time"
    permission_classes = (IsAdminUserOrReadOnly,)

    def find_game_id(self, games, away_team, home_team):
        for game in games:
            if away_team in game.away_team.team_name and home_team in game.home_team.team_name:
                return game.id
        LOG.warning(f"No game found for {away_team} vs {home_team}")
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
        games = Game.objects.order_by("game_time").filter(season=current_season, week=current_week)

        score_list = [
            {
                "game_id": self.find_game_id(games=games, home_team=score[2], away_team=score[0]),
                "away_score": score[1],
                "home_score": score[3],
                "time": score[4],
            }
            for score in scores.values()
        ]

        return Response(score_list)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_fields = ("team_name",)
    ordering = "team_name"
    permission_classes = (IsAdminUserOrReadOnly,)


class PickViewSet(viewsets.ModelViewSet):
    queryset = Pick.objects.all()
    serializer_class = PickSerializer
    pagination_class = APIPagination
    filterset_fields = ("user", "game", "team_to_win")
    ordering = "-id"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            # check if many is required
            if isinstance(data, list):
                kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class RecordsView(APIView):
    permission_classes = (IsAdminUserOrReadOnly,)

    def get(self, request):
        season_id = request.query_params.get("season", None)
        week_id = request.query_params.get("week", None)

        aggregate_list = []
        current_time = timezone.now()

        for user in User.objects.all():
            if user.username == "admin":
                continue

            # First find the number of wins from the Record table
            wins_query = Record.objects.filter(user=user)

            # Then filter by season and week, if necessary
            if season_id:
                wins_query = wins_query.filter(season=season_id)
            if week_id:
                wins_query = wins_query.filter(week=week_id)

            # Finally, find the sum of all the wins in each record
            win_sum = sum([i.wins for i in wins_query])

            # Next find the total number of games from the Pick table
            total_query = Pick.objects.filter(game__game_time__lte=current_time, user=user)

            # Then filter by season and week, if necessary
            if season_id:
                total_query = total_query.filter(game__season=season_id)
            if week_id:
                total_query = total_query.filter(game__week=week_id)

            total_games = total_query.count()
            if total_games == 0:
                continue

            percentage = win_sum / total_games
            aggregate_list.append(
                {
                    "name": user.first_name,
                    "win": win_sum,
                    "loss": total_games - win_sum,
                    "percentage": percentage,
                }
            )

        if week_id:
            totals = sorted(aggregate_list, key=lambda record: record["win"], reverse=True)
        else:
            totals = sorted(aggregate_list, key=lambda record: record["percentage"], reverse=True)

        data = {
            "results": totals,
        }

        return Response(data)


class UpdateView(APIView):
    permission_classes = (IsAdminUserOrReadOnly,)

    def get(self, request):
        from django.core.management import call_command

        call_command("update_records")

        return Response({"status": "success"})
