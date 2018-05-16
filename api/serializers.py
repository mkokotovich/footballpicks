from rest_framework import serializers
from footballseason.models import Game, Team, Pick, Record
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pick
        fields = '__all__'


class PickDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pick
        fields = ('user_name', 'team_to_win')


class GameSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    picks = PickDisplaySerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = '__all__'


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'
