import datetime

from django.db.models import Q
from django.test import TestCase

# Create your tests here.
from complex_queries.models import Competition
from complex_queries.models_tools import parse_search_phrase


class ComplexQuerying(TestCase):

    def setUp(self):
        Competition.objects.create(date=datetime.date(year=2021, month=9, day=3), distance=100, score=1)
        Competition.objects.create(date=datetime.date(year=2021, month=9, day=3), distance=9, score=2)
        Competition.objects.create(date=datetime.date(year=2021, month=9, day=3), distance=20, score=3)
        Competition.objects.create(date=datetime.date(year=2021, month=9, day=3), distance=20, score=3)

    def test_can_query_two_queryset(self):
        search_phrase = "(date gt 2021-09-02) AND ((distance gt 20) OR (distance lt 10))"
        search_filter = parse_search_phrase(search_phrase)
        raw_queryset = Competition.objects.filter(search_filter).order_by('id')

        today = datetime.date(year=2021, month=9, day=2)
        queryset = Competition.objects.filter(Q(date__gt=today) & (Q(distance__gt=20) | Q(distance__lt=10))).order_by('id')
        self.assertQuerysetEqual(raw_queryset, queryset)


    def test_can_query_one_queryset(self):
        search_phrase = "(distance gt 20)"
        search_filter = parse_search_phrase(search_phrase)
        raw_queryset = Competition.objects.filter(search_filter).order_by('id')

        queryset = Competition.objects.filter(Q(distance__gt=20)).order_by('id')
        self.assertQuerysetEqual(raw_queryset, queryset)