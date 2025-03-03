# table_management/urls.py
from django.urls import path
from .views import (
    AvailableTableListView,
    TableReservationView,
    CancelReservationView,
    ReservationHistoryView,
)

urlpatterns = [
    path('', AvailableTableListView.as_view(), name='available-tables'),
    path('<int:pk>/reserve/', TableReservationView.as_view(), name='reserve-table'),
    path('<int:pk>/cancel/', CancelReservationView.as_view(), name='cancel-reservation'),
    path('history/', ReservationHistoryView.as_view(), name='reservation-history'),
]

