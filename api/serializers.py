from rest_framework import serializers
from footballseason.models import Game, Team, Pick, Record


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pick
        fields = '__all__'


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'
