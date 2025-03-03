# restaurant_booking/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('admin/', include('table_management.urls_admin')),
    path('tables/', include('table_management.urls')),
]