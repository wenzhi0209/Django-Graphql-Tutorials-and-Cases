from django.contrib import admin

# Register your models here.
from .models import Deck

class DeckAdmin(admin.ModelAdmin):
    list_display=('id','title','description','last_reviewed',)

admin.site.register(Deck,DeckAdmin)