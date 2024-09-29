from django.urls import path
from .views import AddPointsView, PointsBalanceView, SpendPointsView


urlpatterns = [
    path('add', AddPointsView.as_view(), name='add_points'),
    path('balance', PointsBalanceView.as_view(), name='balance_points'),
    path('spend', SpendPointsView.as_view(), name='spend_points'),
]