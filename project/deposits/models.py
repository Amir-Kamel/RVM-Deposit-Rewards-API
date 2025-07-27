from django.db import models
from django.conf import settings

class Deposit(models.Model):
    MATERIAL_CHOICES = [
        ('plastic', 'Plastic'),
        ('metal', 'Metal'),
        ('glass', 'Glass'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deposits')
    machine_id = models.CharField(max_length=100) #should be a foreign key in another app specially for machines
    material_type = models.CharField(max_length=10, choices=MATERIAL_CHOICES)
    weight_kg = models.FloatField()
    reward_points = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        points_map = {
            'plastic': 1,
            'metal': 3,
            'glass': 2,
        }
        if self.weight_kg is not None and self.material_type:
            self.reward_points = int(self.weight_kg * points_map.get(self.material_type, 0))

        super().save(*args, **kwargs)


class Redemption(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='redemptions')
    used_points = models.PositiveIntegerField()
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='handled_redemptions')
    redeemed_at = models.DateTimeField(auto_now_add=True)