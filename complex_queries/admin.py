from django.contrib import admin

# Register your models here.
from complex_queries.models import Competition


class AdminCompetititon(admin.ModelAdmin):
    list_display = ('id', 'date', 'distance', 'datetime', 'is_win', 'score')


admin.site.register(Competition, AdminCompetititon)
