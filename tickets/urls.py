# urls.py
from django.urls import path,include
from . import views

urlpatterns = [
    path('tickets/create/', views.TicketCreateView.as_view(), name='create_ticket'),
    path('tickets/', views.TicketListView.as_view(), name='ticket_list'),
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('client/search/', views.ClientSearchView.as_view(), name='client_search'),
    path('microsoft/', include('microsoft_auth.urls', namespace='microsoft')),
]