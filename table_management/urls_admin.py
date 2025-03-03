from django.urls import path
from .views import (
    AdminTableListCreateView,
    AdminTableDetailView,
    AdminReservationListView,
)

urlpatterns = [
    path('tables/', AdminTableListCreateView.as_view(), name='admin-tables'),
    path('tables/<int:pk>/', AdminTableDetailView.as_view(), name='admin-table-detail'),
    path('reservations/', AdminReservationListView.as_view(), name='admin-reservations'),
]