from django.contrib import admin
from .models import PQBlock, PQTransaction, PQWallet


admin.site.register(PQBlock)
admin.site.register(PQTransaction)
admin.site.register(PQWallet)

