from .forms import NewsletterForm


def newsletter_form(request):
    """
    Provides the newsletter subscription form globally
    so it's available in all templates (e.g. footer).
    """
    return {"newsletter_form": NewsletterForm()}
