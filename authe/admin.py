from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Define a custom admin class for the User model
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'token_key', 'token_created')

    def token_key(self, obj):
        try:
            token = Token.objects.get(user=obj)
            return token.key
        except Token.DoesNotExist:
            return None
    token_key.short_description = 'Token Key'

    def token_created(self, obj):
        try:
            token = Token.objects.get(user=obj)
            return token.created
        except Token.DoesNotExist:
            return None
    token_created.short_description = 'Token Created'

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)
