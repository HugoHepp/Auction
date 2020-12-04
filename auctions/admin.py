from django.contrib import admin
from .models import Auction, Bids, Comment
# Register your models here.

admin.site.register(Auction)
admin.site.register(Bids)
admin.site.register(Comment)
