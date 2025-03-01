# views.py
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Client, SupportTicket
from .forms import SupportTicketForm
import json

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = SupportTicket
    form_class = SupportTicketForm
    template_name = 'tickets/create_ticket.html'
    success_url = reverse_lazy('ticket_list')
    
    def form_valid(self, form):
        form.instance.submitted_by = self.request.user.email
        return super().form_valid(form)

class ClientSearchView(LoginRequiredMixin, ListView):
    model = Client
    
    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if len(query) >= 4:
            return Client.objects.filter(name__icontains=query)[:7]
        return Client.objects.none()
    
    def render_to_json_response(self, queryset):
        data = list(queryset.values('id', 'name', 'license_key', 'serial_number', 'email', 'phone'))
        return JsonResponse(data, safe=False)
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.render_to_json_response(queryset)

class TicketListView(LoginRequiredMixin, ListView):
    model = SupportTicket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    ordering = ['-created_at']

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = SupportTicket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'