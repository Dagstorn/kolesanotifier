from django.contrib import admin
from .models import Filter, Client
from django.contrib.auth.models import User, Group

admin.site.site_header = "Панель Администратора"

class FilterAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')
    list_display_links = ('title',)
    list_editable = ('text', )
    search_fields = ['title', 'text']
    fields = (
        'title','year_from', 'year_to','price_from', 'price_to','body', 'engine_fuel','transmission_type','engine_volume_from', 'engine_volume_to','text','cheaper_perc', 'view_count',
    )

admin.site.register(Filter, FilterAdmin)
admin.site.register(Client)

admin.site.unregister(User)
admin.site.unregister(Group)

