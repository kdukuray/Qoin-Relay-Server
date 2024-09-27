from django.contrib import admin
from .models import Block, Transaction, Wallet


admin.site.register(Block)
admin.site.register(Transaction)
admin.site.register(Wallet)

