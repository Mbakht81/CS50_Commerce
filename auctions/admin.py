from django.contrib import admin

from auctions.models import Category,Listing,Comment,Bid

# Register your models here.
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)