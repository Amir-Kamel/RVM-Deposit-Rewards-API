from rest_framework import serializers
from .models import Deposit, Redemption
from django.db import models


class DepositSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    reward_points = serializers.ReadOnlyField()
    total_reward_points = serializers.SerializerMethodField()
    total_used_points = serializers.SerializerMethodField()
    remaining_points = serializers.SerializerMethodField()
    total_weight = serializers.SerializerMethodField()


    class Meta:
        model = Deposit
        fields = [
            'id', 'user', 'machine_id', 'material_type', 'weight_kg',
            'reward_points', 'timestamp', 'total_weight',
            'total_reward_points', 'total_used_points', 'remaining_points'
        ]
        read_only_fields = ['reward_points', 'timestamp', 'total_weight' ,'total_reward_points', 'total_used_points', 'remaining_points']

    def validate_weight_kg(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be a positive number.")
        return value

    def get_total_reward_points(self, obj):
        user = obj.user
        return user.deposits.aggregate(total=models.Sum('reward_points'))['total'] or 0

    def get_total_used_points(self, obj):
        user = obj.user
        return user.redemptions.aggregate(total=models.Sum('used_points'))['total'] or 0

    def get_remaining_points(self, obj):
        return self.get_total_reward_points(obj) - self.get_total_used_points(obj)

    def get_total_weight(self, obj):
        user = obj.user
        return user.deposits.aggregate(total=models.Sum('weight_kg'))['total'] or 0
