from .forms import NewsletterForm


def newsletter_form(request):
    """
    Provides the newsletter subscription form globally,
    making it available in all templates that include footer.html.
    """
    return {"newsletter_form": NewsletterForm()}
