from django.http import HttpResponse

from . import models


def index(request):
    # render a template here
    return HttpResponse('loans.')


def submit(request):
    if request.method == 'POST':
        loan = models.Loan(**request.POST)
        # Render JSON response from created Loan object
        loan
    return HttpResponse('loans.')
