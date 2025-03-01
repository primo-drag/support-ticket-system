# models.py
from django.db import models
import datetime
import random
import string

class Client(models.Model):
    name = models.CharField(max_length=255)
    license_key = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name

class SupportTicket(models.Model):
    PROBLEM_TYPES = [
        ('technical', 'Technical Issue'),
        ('billing', 'Billing Issue'),
        ('feature', 'Feature Request'),
        ('question', 'General Question'),
        ('other', 'Other'),
    ]
    
    ticket_id = models.CharField(max_length=11, unique=True, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    problem_type = models.CharField(max_length=20, choices=PROBLEM_TYPES)
    problem_description = models.TextField()
    solution = models.TextField(blank=True, null=True)
    submitted_by = models.EmailField()
    created_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = self.generate_ticket_id()
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        super().save(*args, **kwargs)
    
    def generate_ticket_id(self):
        date_part = datetime.datetime.now().strftime("%Y%m%d")
        while True:
            # Generate 3 random alphanumeric characters
            alpha_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
            ticket_id = f"{date_part}{alpha_part}"
            
            # Check if this ID already exists
            if not SupportTicket.objects.filter(ticket_id=ticket_id).exists():
                return ticket_id