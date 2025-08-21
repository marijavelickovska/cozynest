from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ContactMessage model.
    Displays sender name, email and message,
    allows search and filtering by name and email.
    """
    list_display = ('name', 'email', 'message', 'created_on')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_on',)
