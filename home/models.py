from django.db import models


class ContactMessage(models.Model):
    """
    Stores messages sent by users via the contact form.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Newsletter(models.Model):
    """
    Stores email addresses subscribed to the newsletter.
    """
    email = models.EmailField(unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
