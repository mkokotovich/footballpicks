import logging

from rest_framework import serializers
from footballseason.models import Game, Team, Pick, Record
from django.contrib.auth.models import User


LOG = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PickSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Pick
        fields = '__all__'
        read_only_fields = ('date_submitted', 'user')

    def create(self, validated_data):
        LOG.info(self.context['request'].user)
        user = self.context['request'].user
        pick, created = Pick.objects.get_or_create(
            user=user,
            game=validated_data['game'],
            defaults={
                'team_to_win': validated_data['team_to_win'],
            }
        )
        LOG.info(f"pick {pick} created: {created}. New team_to_win: {validated_data['team_to_win']}")
        if not created:
            pick.team_to_win = validated_data['team_to_win']
            pick.save()
        return pick


class PickDisplaySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Pick
        fields = ('user', 'team_to_win')


class GameSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    picks = PickDisplaySerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = '__all__'
