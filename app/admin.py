from django.contrib import admin

from .models import CustomUser, EmailVerification, Product

admin.site.register(CustomUser)
admin.site.register(EmailVerification)
admin.site.register(Product)
