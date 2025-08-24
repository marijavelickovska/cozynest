from django.contrib import admin
from .models import ContactMessage, Newsletter


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


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Newsletter model.
    Displays subscriber emails and the date they subscribed.
    """
    list_display = ("email", "created_at")
    search_fields = ("email",)
    ordering = ("-created_at",)
