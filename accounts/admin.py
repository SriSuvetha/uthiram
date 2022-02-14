from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Donor
from reversion.admin import VersionAdmin


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name','phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'phone', 'is_staff')
    search_fields = ('email', 'name', 'phone')
    ordering = ('email',)


admin.site.register(get_user_model(), CustomUserAdmin)

@admin.register(Donor)
class ClientModelAdmin(VersionAdmin):
    list_display = ('donorid', 'email','name', 'blood', 'age','phone', 'city',
                    'district', 'state', 'country', 'pincode', 'available', 'eligible_date')
                    #'district', 'state', 'country', 'pincode', 'rollno', 'instituition', 'available', 'eligible_date')