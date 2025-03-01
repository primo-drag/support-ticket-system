# admin.py
from django.contrib import admin
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import csv
import io
from .models import Client, SupportTicket

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_key', 'serial_number', 'email', 'phone')
    search_fields = ('name', 'license_key', 'serial_number', 'email')
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls
    
    def import_csv(self, request):
        if request.method == 'POST':
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data['csv_file']
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                
                count = 0
                for row in reader:
                    Client.objects.create(
                        name=row.get('name', ''),
                        license_key=row.get('license_key', ''),
                        serial_number=row.get('serial_number', ''),
                        email=row.get('email', ''),
                        phone=row.get('phone', '')
                    )
                    count += 1
                
                messages.success(request, f'Successfully imported {count} clients')
                return redirect('..')
        else:
            form = CsvImportForm()
        
        template = 'admin/csv_import.html'
        context = {
            'form': form,
        }
        return render(request, template, context)

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'client', 'problem_type', 'created_at', 'submitted_by')
    search_fields = ('ticket_id', 'client__name', 'problem_description')
    list_filter = ('problem_type', 'created_at')