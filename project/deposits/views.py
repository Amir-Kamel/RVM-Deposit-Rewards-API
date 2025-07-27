from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from .models import Deposit, Redemption
from .serializers import DepositSerializer
from .utils import send_deposit_summary_email
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class DepositCreateView(generics.CreateAPIView):
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        deposits = Deposit.objects.filter(user=user)

        if not deposits:
            return Response({
                "username": user.username,
                "total_recycled_weight_kg": 0,
                "total_reward_points": 0,
                "total_used_points": 0,
                "remaining_points": 0,
            })

        deposit_instance = deposits.latest('timestamp')
        serializer = DepositSerializer(deposit_instance, context={'request': request})

        return Response({
            "username": user.username,
            "total_recycled_weight_kg": serializer.get_total_weight(deposit_instance),
            "total_reward_points": serializer.get_total_reward_points(deposit_instance),
            "total_used_points": serializer.get_total_used_points(deposit_instance),
            "remaining_points": serializer.get_remaining_points(deposit_instance),
        })


class SendDepositSummaryEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user.is_verified:
            return Response({"error": "Email not verified. Cannot send summary."}, status=400)
        deposits = Deposit.objects.filter(user=user)

        if not deposits.exists():
            return Response({"detail": "No deposits found for user."}, status=status.HTTP_404_NOT_FOUND)
        deposit_instance = deposits.latest('timestamp')
        serializer = DepositSerializer(deposit_instance)

        total_reward_points = serializer.get_total_reward_points(deposit_instance)
        total_used_points = serializer.get_total_used_points(deposit_instance)
        remaining_points = serializer.get_remaining_points(deposit_instance)
        total_weight = serializer.get_total_weight(deposit_instance)

        send_deposit_summary_email(user, total_weight, total_reward_points, total_used_points, remaining_points)

        return Response({
            "detail": "Summary email sent successfully.",
            "total_weight": total_weight,
            "total_reward_points": total_reward_points,
            "total_used_points": total_used_points,
            "remaining_points": remaining_points
        }, status=status.HTTP_200_OK)


class DeductRewardPointsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        user_id = request.data.get("user_id")
        points_to_deduct = int(request.data.get("points", 0))

        if not user_id or points_to_deduct <= 0:
            return Response({"error": "User ID and valid points are required."}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        deposits = Deposit.objects.filter(user=user)
        if not deposits.exists():
            return Response({"error": "User has no deposits, so no reward points to deduct."}, status=400)

        deposit_instance = deposits.latest('timestamp')
        serializer = DepositSerializer(deposit_instance)
        remaining_points = serializer.get_remaining_points(deposit_instance)

        if points_to_deduct > remaining_points:
            return Response({"error": "User doesn't have enough reward points."}, status=400)

        Redemption.objects.create(user=user, used_points=points_to_deduct, staff=request.user)

        updated_remaining = remaining_points - points_to_deduct

        return Response({
            "message": f"{points_to_deduct} points deducted from user {user.username}.",
            "remaining_points": updated_remaining
        })

