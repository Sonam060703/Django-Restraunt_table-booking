# table_management/views.py
from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import date

from .models import Table, Reservation
from .serializers import TableSerializer, ReservationSerializer
from .permissions import IsAdmin, IsOwnerOrAdmin

# Admin Views
class AdminTableListCreateView(generics.ListCreateAPIView):
    """Admin endpoint for listing and creating tables"""
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'location']
    ordering_fields = ['capacity', 'name', 'created_at']

class AdminTableDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin endpoint for retrieving, updating and deleting a table"""
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class AdminReservationListView(generics.ListAPIView):
    """Admin endpoint for viewing all reservations"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'table__name', 'status']
    ordering_fields = ['reservation_date', 'start_time', 'created_at']

# User Views
class AvailableTableListView(generics.ListAPIView):
    """User endpoint for viewing available tables"""
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only available tables"""
        queryset = Table.objects.filter(is_available=True)
        
        # Filter by capacity if provided
        capacity = self.request.query_params.get('capacity')
        if capacity:
            queryset = queryset.filter(capacity__gte=int(capacity))
            
        # Filter by date/time if provided
        reservation_date = self.request.query_params.get('date')
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')
        
        if reservation_date and start_time and end_time:
            # Find tables with conflicting reservations
            conflicting_tables = Reservation.objects.filter(
                reservation_date=reservation_date,
                status__in=['pending', 'confirmed'],
            ).filter(
                # Time overlap condition
                start_time__lt=end_time,
                end_time__gt=start_time
            ).values_list('table_id', flat=True)
            
            # Exclude those tables
            queryset = queryset.exclude(id__in=conflicting_tables)
            
        return queryset

class TableReservationView(APIView):
    """User endpoint for reserving a table"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        table = get_object_or_404(Table, pk=pk, is_available=True)
        
        # Create reservation data
        reservation_data = {
            'table': table,
            'user': request.user,
            **request.data
        }
        
        serializer = ReservationSerializer(data=reservation_data)
        if serializer.is_valid():
            serializer.save(user=request.user, table=table, status='confirmed')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CancelReservationView(APIView):
    """User endpoint for canceling a reservation"""
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def delete(self, request, pk):
        table = get_object_or_404(Table, pk=pk)
        reservation = get_object_or_404(
            Reservation,
            table=table,
            user=request.user,
            status__in=['pending', 'confirmed']
        )
        
        # Mark as cancelled instead of deleting
        reservation.status = 'cancelled'
        reservation.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReservationHistoryView(generics.ListAPIView):
    """User endpoint for viewing reservation history"""
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only user's reservations"""
        return Reservation.objects.filter(user=self.request.user)