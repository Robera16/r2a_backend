from django.urls import path
from .views import MyAdminRequests, create_admin_ticket, delete_admin_ticket, get_admin_ticket

urlpatterns = [
    path('my_admin_tickets/', MyAdminRequests.as_view()),
    path('create_ticket/', create_admin_ticket),
    path('delete_admin_ticket/<int:pk>/', delete_admin_ticket),
    path('get_admin_ticket/<int:pk>/', get_admin_ticket)
]