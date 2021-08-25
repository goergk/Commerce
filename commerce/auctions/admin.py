from django.contrib import admin

from .models import *

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
      exclude = ('actual_price',)

admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment)
admin.site.register(Bid)

# Optional to add new category
# admin.site.register(Category)

