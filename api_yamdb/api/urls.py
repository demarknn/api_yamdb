from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'DELETE', 'POST'])
def genre(request):
    pass