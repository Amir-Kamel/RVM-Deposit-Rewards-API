from django.urls import path
from .views import DepositCreateView, UserSummaryView, SendDepositSummaryEmailView, DeductRewardPointsView

urlpatterns = [
    path('deposit/', DepositCreateView.as_view(), name='deposit'),
    path('summary/', UserSummaryView.as_view(), name='user-summary'),
    path('send-email-summary/', SendDepositSummaryEmailView.as_view(), name='send-deposit-summary'),
    path('deduct-points/', DeductRewardPointsView.as_view(), name='deduct-points'),
]
