from django.shortcuts import render
from django.views.generic.edit import FormView
from . import forms
from django.urls import reverse_lazy
from django.contrib import messages


class ContactView(FormView):
    template_name = "contact/contact.html"
    form_class = forms.ContactForm
    success_url = reverse_lazy('contact_app:contact')

    def form_valid(self, form):        
        # Try to send email and handle any errors if they occur
        return super().form_valid(form)
    
