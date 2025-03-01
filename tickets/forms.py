# forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import SupportTicket, Client

class SupportTicketForm(forms.ModelForm):
    client_search = forms.CharField(
        label="Search Client (by name, license key, or serial number)",
        required=False,
        widget=forms.TextInput(attrs={'class': 'client-search'})
    )
    
    class Meta:
        model = SupportTicket
        fields = ['client', 'problem_type', 'problem_description', 'solution', 'created_at']
        widgets = {
            'client': forms.HiddenInput(),
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_at'].required = False
        self.fields['solution'].required = False
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'client_search',
            'client',
            Row(
                Column('problem_type', css_class='form-group col-md-6'),
                Column('created_at', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'problem_description',
            'solution',
            Submit('submit', 'Create Ticket', css_class='btn btn-primary')
        )