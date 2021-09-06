import datetime
import math
import re

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from complex_queries.models import Competition
from complex_queries.models_tools import parse_search_phrase


class TestView(APIView):
    def get(self, request, *args, **kwargs):

        # search_phrase = "(date gt 2021-09-03) AND ((distance gt 20) OR (distance lt 10))"
        search_phrase = request.GET.get('search_phrase')
        if search_phrase:
            search_filter = parse_search_phrase(search_phrase)
            queryset = Competition.objects.filter(search_filter)
            return Response('ok')
        else:
            return Response("Search phrase doesn't exist")
