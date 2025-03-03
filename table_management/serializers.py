# table_management/serializers.py
from rest_framework import serializers
from pydantic import BaseModel, validator, Field
from datetime import date, datetime
from .models import Table, Reservation

# Pydantic models for validation
class TableSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    capacity: int = Field(..., gt=0)
    location: str = Field(default="")
    is_available: bool = Field(default=True)

class ReservationSchema(BaseModel):
    reservation_date: date
    start_time: str
    end_time: str
    party_size: int = Field(..., gt=0)
    special_requests: str = Field(default="")
    
    @validator('reservation_date')
    def validate_date(cls, v):
        if v < date.today():
            raise ValueError('Reservation date cannot be in the past')
        return v
    
    @validator('party_size')
    def validate_party_size(cls, v):
        if v <= 0:
            raise ValueError('Party size must be greater than 0')
        return v

# DRF Serializers
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate(self, data):
        # Using Pydantic for validation
        TableSchema(**data)
        return data

class ReservationSerializer(serializers.ModelSerializer):
    table_name = serializers.CharField(source='table.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'user', 'status', 'table_name', 'username')
    
    def validate(self, data):
        # Using Pydantic for validation
        ReservationSchema(
            reservation_date=data['reservation_date'],
            start_time=data['start_time'].strftime('%H:%M'),
            end_time=data['end_time'].strftime('%H:%M'),
            party_size=data['party_size'],
            special_requests=data.get('special_requests', '')
        )
        
        # Check if the table is available
        table = data['table']
        if not table.is_available:
            raise serializers.ValidationError("This table is not available for reservations")
        
        # Check if the party size exceeds table capacity
        if data['party_size'] > table.capacity:
            raise serializers.ValidationError(f"Party size exceeds table capacity ({table.capacity})")
        
        # Check for time conflicts
        conflicting_reservations = Reservation.objects.filter(
            table=table,
            reservation_date=data['reservation_date'],
            status__in=['pending', 'confirmed'],
        ).exclude(pk=self.instance.pk if self.instance else None)
        
        for reservation in conflicting_reservations:
            if (data['start_time'] < reservation.end_time and 
                data['end_time'] > reservation.start_time):
                raise serializers.ValidationError(
                    f"This table is already reserved from {reservation.start_time} to {reservation.end_time}"
                )
        
        return data