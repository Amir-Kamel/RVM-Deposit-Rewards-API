from django.contrib import admin
from .models import Deposit, Redemption

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    readonly_fields = ('reward_points', 'timestamp')
    list_display = ('user', 'material_type', 'weight_kg', 'reward_points', 'timestamp')

@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'used_points', 'staff', 'redeemed_at')
