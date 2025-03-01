# management/commands/import_clients.py
import csv
from django.core.management.base import BaseCommand
from tickets.models import Client

class Command(BaseCommand):
    help = 'Import clients from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
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
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} clients'))