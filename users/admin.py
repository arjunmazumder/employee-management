from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Designation, Team, Notice
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'name', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'address', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
# admin.site.register(Designation)
admin.site.register(Team)
admin.site.register(Notice)
